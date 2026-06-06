from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
            "id",
            "room_number",
            "floor",
            "room_type",
            "capacity",
            "price_per_night",
            "status",
            "description",
            "created_at",
            "updated_at",
        )
        # read_only_fields = ["hotel"]


    def validate(self, attrs):

        hotel = self.context["request"].user.hotel
        room_number = attrs.get("room_number")

        queryset = Room.objects.filter(
            hotel=hotel,
            room_number=room_number
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "This room number already exists."
            )

        return attrs