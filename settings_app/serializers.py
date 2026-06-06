from rest_framework import serializers

from .models import HotelSetting


class HotelSettingSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = HotelSetting

        fields = (
            "id",
            "check_in_time",
            "check_out_time",
            "currency",
            "timezone",
            "tax_percentage",
            "created_at",
            "updated_at",
        )