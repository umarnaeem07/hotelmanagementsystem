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

        return Response(serializer.data)

    def delete(self, request, pk):

        reservation = self.get_object(
            request,
            pk
        )

        reservation.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class CheckInAPIView(APIView):

    permission_classes = [IsAuthenticated,IsReceptionistOrAbove]

    def post(self, request, pk):

        reservation = Reservation.objects.get(
            pk=pk,
            hotel=request.user.hotel
        )

        if reservation.status != "reserved":

            return Response(
                {
                    "message":
                    "Only reserved bookings can be checked in."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = "checked_in"
        reservation.save()

        room = reservation.room
        room.status = "occupied"
        room.save()

        return Response(
            {
                "message":
                "Guest checked in successfully."
            }
        )
class CheckOutAPIView(APIView):

    permission_classes = [IsAuthenticated,IsReceptionistOrAbove]

    def post(self, request, pk):

        reservation = Reservation.objects.get(
            pk=pk,
            hotel=request.user.hotel
        )

        if reservation.status != "checked_in":

            return Response(
                {
                    "message":
                    "Guest is not checked in."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = "checked_out"
        reservation.save()

        room = reservation.room
        room.status = "available"
        room.save()

        return Response(
            {
                "message":
                "Guest checked out successfully."
            }
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

        serializer.save(
            reservation=reservation
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

        return Response(
            {
                "message":
                "Service removed successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )