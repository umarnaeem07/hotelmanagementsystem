from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import HotelService, ReservationService
from .serializers import HotelServiceSerializer, ReservationServiceSerializer

# Optional: use your role-based permission
from staff.permissions import IsManagerOrOwner
from reservations.models import Reservation

class HotelServiceListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsManagerOrOwner
    ]

    def get(
        self,
        request
    ):

        services = HotelService.objects.filter(
            hotel=request.user.hotel
        )

        serializer = HotelServiceSerializer(
            services,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(
        self,
        request
    ):

        serializer = HotelServiceSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            hotel=request.user.hotel
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class HotelServiceDetailAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated,IsManagerOrOwner
    ]

    def get_object(
        self,request,pk):
            return HotelService.objects.get(
            pk=pk,
            hotel=request.user.hotel
        )

    def get(
        self,
        request,
        pk
    ):

        service = self.get_object(
            request,
            pk
        )

        serializer = HotelServiceSerializer(
            service
        )

        return Response(
            serializer.data
        )

    def put(
        self,
        request,
        pk
    ):

        service = self.get_object(
            request,
            pk
        )

        serializer = HotelServiceSerializer(
            service,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data
        )

    def delete(
        self,
        request,
        pk
    ):

        service = self.get_object(
            request,
            pk
        )

        service.delete()

        return Response(
            {
                "message":
                "Service deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )

class AddReservationServiceAPIView(
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

        try:
            reservation = Reservation.objects.get(
                pk=reservation_id,
                hotel=request.user.hotel
            )

        except Reservation.DoesNotExist:

            return Response(
                {
                    "message":
                    "Reservation not found."
                },
                status=status.HTTP_404_NOT_FOUND
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

        # Security check:
        # Service must belong to the same hotel.
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

class ReservationServiceListAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        reservation_id
    ):

        try:
            reservation = Reservation.objects.get(
                pk=reservation_id,
                hotel=request.user.hotel
            )

        except Reservation.DoesNotExist:

            return Response(
                {
                    "message":
                    "Reservation not found."
                },
                status=status.HTTP_404_NOT_FOUND
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

