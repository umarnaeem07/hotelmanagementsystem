from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(ModelViewSet):

    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Reservation.objects.filter(
            hotel=self.request.user.hotel
        )

    def perform_create(self, serializer):

        reservation = serializer.save(
            hotel=self.request.user.hotel
        )

        nights = (
            reservation.check_out -
            reservation.check_in
        ).days

        reservation.total_amount = (
            reservation.room.price_per_night * nights
        )

        reservation.save()