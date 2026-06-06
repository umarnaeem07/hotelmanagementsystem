from django.contrib import admin

from .models import HotelSetting


@admin.register(HotelSetting)
class HotelSettingAdmin(admin.ModelAdmin):

    list_display = (
        "hotel",
        "currency",
        "timezone",
        "check_in_time",
        "check_out_time",
        "tax_percentage",
    )

    search_fields = (
        "hotel__name",
    )

    list_filter = (
        "currency",
        "timezone",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )