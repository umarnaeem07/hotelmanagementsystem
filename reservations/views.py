from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer, ReservationServiceSerializer
from rest_framework.views import APIView
from staff.permissions import IsReceptionistOrAbove
from services.models import (
    HotelService,
    ReservationService
)
from django.shortcuts import get_object_or_404
from invoices.models import Invoice
from activity_logs.services import (
    log_activity
)


class ReservationListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsReceptionistOrAbove]

    def get(self, request):

        reservations = Reservation.objects.filter(
            hotel=request.user.hotel
        )

        serializer = ReservationSerializer(
            reservations,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ReservationSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        reservation = serializer.save(
            hotel=request.user.hotel
        )

        nights = (
            reservation.check_out -
            reservation.check_in
        ).days

        reservation.total_amount = (
            reservation.room.price_per_night * nights
        )

        reservation.save()
        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="created",
            object_type="Reservation",
            object_id=reservation.id,
            description=f"Reservation created for {reservation.id}"
        )

        return Response(
            ReservationSerializer(reservation).data,
            status=status.HTTP_201_CREATED
        )
class ReservationDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsReceptionistOrAbove]

    def get_object(self, request, pk):

        return Reservation.objects.get(
            pk=pk,
            hotel=request.user.hotel
        )

    def get(self, request, pk):

        reservation = self.get_object(
            request,
            pk
        )

        serializer = ReservationSerializer(
            reservation
        )

        return Response(serializer.data)

    def put(self, request, pk):

        reservation = self.get_object(
            request,
            pk
        )

        serializer = ReservationSerializer(
            reservation,
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        reservation = serializer.save()

        nights = (
            reservation.check_out -
            reservation.check_in
        ).days

        reservation.total_amount = (
            reservation.room.price_per_night * nights
        )

        reservation.save()
        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="updated",
            object_type="Reservation",
            object_id=reservation.id,
            description=f"Reservation updated for {reservation.id}"
        )
        return Response(serializer.data)

    def delete(self, request, pk):

        reservation = self.get_object(
            request,
            pk
        )

        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="deleted",
            object_type="Reservation",
            object_id=reservation.id,
            description=f"Reservation deleted for {reservation.id}"
        )
        reservation.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class CheckInAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsReceptionistOrAbove
    ]

    def post(self, request, pk):

        reservation = get_object_or_404(
            Reservation,
            pk=pk,
            hotel=request.user.hotel
        )

        # STEP 1: Only reserved bookings
        if reservation.status != "reserved":
            return Response(
                {
                    "message": "Only reserved bookings can be checked in."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # STEP 2: Get ROOM invoice
        room_invoice = Invoice.objects.filter(
            reservation=reservation,
            invoice_type="room"
        ).first()

        if not room_invoice:
            return Response(
                {
                    "message": "Room invoice not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # STEP 3: STRICT PAYMENT CHECK
        if room_invoice.payment_status != "paid":
            return Response(
                {
                    "message": "Check-in denied. Full payment required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # STEP 4: CHECK-IN
        reservation.status = "checked_in"
        reservation.save()

        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="checked_in",
            object_type="Reservation",
            object_id=reservation.id,
            description=f"Guest checked in for {reservation.id}"
        )

        # STEP 5: ROOM STATUS UPDATE
        room = reservation.room
        room.status = "occupied"
        room.save()

        

        return Response(
            {
                "message": "Guest checked in successfully."
            },
            status=status.HTTP_200_OK
        )
class CheckOutAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsReceptionistOrAbove
    ]

    def post(self, request, pk):

        reservation = get_object_or_404(
            Reservation,
            pk=pk,
            hotel=request.user.hotel
        )

        # STEP 1: Must be checked in
        if reservation.status != "checked_in":
            return Response(
                {
                    "message": "Only checked-in guests can check out."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # STEP 2: Get ALL invoices
        invoices = Invoice.objects.filter(
            reservation=reservation
        )

        if not invoices.exists():
            return Response(
                {
                    "message": "No invoices found for this reservation."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # STEP 3: Check unpaid invoices
        unpaid_invoices = invoices.filter(
            payment_status="unpaid"
        )

        if unpaid_invoices.exists():
            return Response(
                {
                    "message": (
                        "Check-out blocked. "
                        "All invoices must be paid before checkout."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # STEP 4: UPDATE STATUS
        reservation.status = "checked_out"
        reservation.save()

        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="checked_out",
            object_type="Reservation",
            object_id=reservation.id,
            description=f"Guest checked out for {reservation.id}"
        )

        # STEP 5: FREE ROOM
        room = reservation.room
        room.status = "available"
        room.save()

        return Response(
            {
                "message": "Check-out successful.",
                "reservation_id": reservation.id,
                "status": reservation.status
            },
            status=status.HTTP_200_OK
        )
class ReservationServiceAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        reservation_id
    ):

        reservation = get_object_or_404(
            Reservation,
            pk=reservation_id,
            hotel=request.user.hotel
        )

        serializer = (
            ReservationServiceSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        service = serializer.validated_data[
            "service"
        ]

        # Make sure the selected
        # service belongs to this hotel.
        if (
            service.hotel !=
            request.user.hotel
        ):
            return Response(
                {
                    "message":
                    "Invalid hotel service."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation_service = serializer.save(
            reservation=reservation
        )

        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="created",
            object_type="ReservationService",
            object_id=reservation_service.id,
            description=f"Service added to reservation for {reservation.id}"
        )

        

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    def get(
        self,
        request,
        reservation_id
    ):

        reservation = get_object_or_404(
            Reservation,
            pk=reservation_id,
            hotel=request.user.hotel
        )

        services = (
            ReservationService.objects.filter(
                reservation=reservation
            )
        )

        serializer = (
            ReservationServiceSerializer(
                services,
                many=True
            )
        )

        return Response(
            serializer.data
        )
class ReservationServiceDetailAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]
    def get(
        self,
        request,
        reservation_id,
        service_id
    ):
        

        reservation = get_object_or_404(
            Reservation,
            pk=reservation_id,
            hotel=request.user.hotel
        )

        reservation_service = (
            get_object_or_404(
                ReservationService,
                pk=service_id,
                reservation=reservation
            )
        )

        serializer = (
            ReservationServiceSerializer(
                reservation_service
            )
        )

        return Response(serializer.data)

    def delete(
        self,
        request,
        reservation_id,
        service_id
    ):

        reservation = get_object_or_404(
            Reservation,
            pk=reservation_id,
            hotel=request.user.hotel
        )

        reservation_service = (
            get_object_or_404(
                ReservationService,
                pk=service_id,
                reservation=reservation
            )
        )

        reservation_service.delete()
    
        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="deleted",
            object_type="ReservationService",
            object_id=reservation_service.id,
            description=f"Service removed from reservation for {reservation.id}"
        )

        return Response(
            {
                "message":
                "Service removed successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )