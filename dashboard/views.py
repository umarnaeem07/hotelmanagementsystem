from datetime import date

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rooms.models import Room
from guests.models import Guest
from reservations.models import Reservation
from housekeeping.models import HousekeepingTask

from .serializers import DashboardSerializer


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        hotel = request.user.hotel

        total_rooms = Room.objects.filter(
            hotel=hotel
        ).count()

        available_rooms = Room.objects.filter(
            hotel=hotel,
            status="available"
        ).count()

        occupied_rooms = Room.objects.filter(
            hotel=hotel,
            status="occupied"
        ).count()

        maintenance_rooms = Room.objects.filter(
            hotel=hotel,
            status="maintenance"
        ).count()

        cleaning_rooms = Room.objects.filter(
            hotel=hotel,
            status="cleaning"
        ).count()

        total_guests = Guest.objects.filter(
            hotel=hotel
        ).count()

        active_reservations = Reservation.objects.filter(
            hotel=hotel,
            status__in=[
                "confirmed",
                "checked_in"
            ]
        ).count()

        today = date.today()

        today_checkins = Reservation.objects.filter(
            hotel=hotel,
            check_in=today
        ).count()

        today_checkouts = Reservation.objects.filter(
            hotel=hotel,
            check_out=today
        ).count()

        pending_housekeeping_tasks = (
            HousekeepingTask.objects.filter(
                room__hotel=hotel,
                completed=False
            ).count()
        )

        data = {
            "total_rooms": total_rooms,
            "available_rooms": available_rooms,
            "occupied_rooms": occupied_rooms,
            "maintenance_rooms": maintenance_rooms,
            "cleaning_rooms": cleaning_rooms,
            "total_guests": total_guests,
            "active_reservations": active_reservations,
            "today_checkins": today_checkins,
            "today_checkouts": today_checkouts,
            "pending_housekeeping_tasks": pending_housekeeping_tasks,
        }

        serializer = DashboardSerializer(data)

        return Response(serializer.data)