from rest_framework import serializers
from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(
        source="owner.username",
        read_only=True
    )
    class Meta:
        model = Hotel
        fields = "__all__"
        read_only_fields = (
            "owner",
            "created_at",
            "updated_at",
        )