from rest_framework import serializers
from .models import HousekeepingTask


class HousekeepingTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = HousekeepingTask
        fields = "__all__"

        read_only_fields = (
            "hotel",
            "created_at",
            "updated_at",
        )
        def validate_room(self, value):

            hotel = self.context["request"].user.hotel

            if value.hotel != hotel:
                raise serializers.ValidationError(
                    "Room does not belong to your hotel."
                )

            return value