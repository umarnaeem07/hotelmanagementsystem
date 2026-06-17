from django.db import models


class HotelService(models.Model):

    SERVICE_TYPES = (
        ("free", "Free"),
        ("paid", "Paid"),
    )

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="services"
    )

    name = models.CharField(
        max_length=100
    )

    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_TYPES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class ReservationService(models.Model):

    reservation = models.ForeignKey(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="services"
    )

    service = models.ForeignKey(
        "services.HotelService",
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(
        self,
        *args,
        **kwargs
    ):

        self.total_price = (
            self.service.price *
            self.quantity
        )

        super().save(
            *args,
            **kwargs
        )

