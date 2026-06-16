from rest_framework import serializers
from .models import HotelService, ReservationService


class HotelServiceSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = HotelService

        fields = "__all__"

        read_only_fields = (
            "id",
            "hotel",
            "created_at",
        )
class ReservationServiceSerializer(
    serializers.ModelSerializer
):

    service_name = serializers.CharField(
        source="service.name",
        read_only=True
    )

    class Meta:

        model = ReservationService

        fields = (
            "id",
            "reservation",
            "service",
            "service_name",
            "quantity",
            "total_price",
            "created_at",
        )

        read_only_fields = (
            "id",
            "total_price",
            "created_at",
        )