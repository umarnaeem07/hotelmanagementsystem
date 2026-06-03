from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "guest",
        "room",
        "check_in",
        "check_out",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "guest__first_name",
        "guest__last_name",
        "room__room_number",
    )