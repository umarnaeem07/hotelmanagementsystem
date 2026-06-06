from django.db.models import Sum, Count, Avg

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rooms.models import Room
from payments.models import Payment
from reservations.models import Reservation

class RevenueReportAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        payments = Payment.objects.filter(
            reservation__hotel=request.user.hotel
        )

        data = payments.aggregate(
            total_revenue=Sum("amount"),
            total_payments=Count("id"),
            average_payment=Avg("amount")
        )

        return Response(data)
class OccupancyReportAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        rooms = Room.objects.filter(
            hotel=request.user.hotel
        )

        total_rooms = rooms.count()

        occupied_rooms = rooms.filter(
            status="occupied"
        ).count()

        available_rooms = rooms.filter(
            status="available"
        ).count()

        occupancy_rate = 0

        if total_rooms > 0:

            occupancy_rate = (
                occupied_rooms /
                total_rooms
            ) * 100

        return Response({
            "total_rooms": total_rooms,
            "occupied_rooms": occupied_rooms,
            "available_rooms": available_rooms,
            "occupancy_rate": round(
                occupancy_rate,
                2
            )
        })
class ReservationReportAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        reservations = Reservation.objects.filter(
            hotel=request.user.hotel
        )

        return Response({

            "total_reservations":
                reservations.count(),

            "reserved":
                reservations.filter(
                    status="reserved"
                ).count(),

            "checked_in":
                reservations.filter(
                    status="checked_in"
                ).count(),

            "checked_out":
                reservations.filter(
                    status="checked_out"
                ).count(),

            "cancelled":
                reservations.filter(
                    status="cancelled"
                ).count(),
        })