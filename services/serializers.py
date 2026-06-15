from rest_framework import serializers
from .models import HotelService


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