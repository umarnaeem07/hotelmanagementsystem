from django.contrib import admin
from .models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "owner",
        "phone",
        "email",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "owner__username",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
    def __str__(self):
        return super().__str__()
    