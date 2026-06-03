from django.contrib import admin
from .models import HousekeepingTask


@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "room",
        "title",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "room__room_number",
        "title",
    )