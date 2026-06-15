from datetime import date

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rooms.models import Room
from reservations.models import Reservation

from .serializers import AnalyticsSerializer
from staff.permissions import IsManagerOrOwner


class AnalyticsAPIView(APIView):

    permission_classes = [IsAuthenticated, IsManagerOrOwner]

    def get(self, request):

        hotel = request.user.hotel

        total_rooms = Room.objects.filter(
            hotel=hotel
        ).count()

        occupied_rooms = Room.objects.filter(
            hotel=hotel,
            status="occupied"
        ).count()

        occupancy_rate = 0

        if total_rooms > 0:
            occupancy_rate = (
                occupied_rooms / total_rooms
            ) * 100

        total_bookings = Reservation.objects.filter(
            hotel=hotel
        ).count()

        today = date.today()

        monthly_revenue = (
            Reservation.objects.filter(
                hotel=hotel,
                check_in__year=today.year,
                check_in__month=today.month,
                status__in=[
                    "confirmed",
                    "checked_in",
                    "checked_out"
                ]
            ).aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        )

        reservations = Reservation.objects.filter(
            hotel=hotel
        )

        total_days = 0

        for reservation in reservations:

            total_days += (
                reservation.check_out -
                reservation.check_in
            ).days

        average_stay_duration = 0

        if reservations.count() > 0:
            average_stay_duration = (
                total_days /
                reservations.count()
            )

        data = {
            "occupancy_rate": round(
                occupancy_rate,
                2
            ),
            "total_bookings": total_bookings,
            "monthly_revenue": monthly_revenue,
            "average_stay_duration": round(
                average_stay_duration,
                2
            )
        }

        serializer = AnalyticsSerializer(data)

        return Response(serializer.data)