from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_number",
        "hotel",
        "room_type",
        "status",
        "price_per_night",
    )

    search_fields = (
        "room_number",
    )

    list_filter = (
        "status",
        "room_type",
    )