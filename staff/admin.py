from django.contrib import admin
from .models import Staff, StaffInvitation


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "hotel",
        "role",
        "is_active",
    )


@admin.register(StaffInvitation)
class StaffInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "hotel",
        "role",
        "accepted",
        "invited_by",
        "created_at",
    )

    list_filter = (
        "role",
        "accepted",
    )

    search_fields = (
        "email",
        "hotel__name",
    )