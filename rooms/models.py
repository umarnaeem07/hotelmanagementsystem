from django.db import models


class Room(models.Model):

    STATUS_CHOICES = (
        ("available", "Available"),
        ("occupied", "Occupied"),
        ("maintenance", "Maintenance"),
        ("cleaning", "Cleaning"),
    )

    ROOM_TYPE_CHOICES = (
        ("standard", "Standard"),
        ("deluxe", "Deluxe"),
        ("suite", "Suite"),
    )

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_number = models.CharField(
        max_length=20
    )

    floor = models.IntegerField()

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPE_CHOICES
    )

    capacity = models.PositiveIntegerField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hotel", "room_number"],
                name="unique_room_per_hotel"
            )
        ]

    def __str__(self):
        return f"Room {self.room_number}"