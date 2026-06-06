from rest_framework import serializers


class AnalyticsSerializer(serializers.Serializer):

    occupancy_rate = serializers.FloatField()

    total_bookings = serializers.IntegerField()

    monthly_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    average_stay_duration = serializers.FloatField()