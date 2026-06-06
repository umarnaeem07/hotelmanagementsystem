from django.db import models


class HotelSetting(models.Model):

    hotel = models.OneToOneField(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="settings"
    )

    check_in_time = models.TimeField()

    check_out_time = models.TimeField()

    currency = models.CharField(
        max_length=10,
        default="PKR"
    )

    timezone = models.CharField(
        max_length=100,
        default="Asia/Karachi"
    )

    tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.hotel.name} Settings"