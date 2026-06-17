from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    total_rooms = serializers.IntegerField()
    available_rooms = serializers.IntegerField()
    occupied_rooms = serializers.IntegerField()
    maintenance_rooms = serializers.IntegerField()
    cleaning_rooms = serializers.IntegerField()

    total_guests = serializers.IntegerField()

    active_reservations = serializers.IntegerField()
    today_checkins = serializers.IntegerField()
    today_checkouts = serializers.IntegerField()

    pending_housekeeping_tasks = serializers.IntegerField()

    unpaid_invoices_count = serializers.IntegerField()