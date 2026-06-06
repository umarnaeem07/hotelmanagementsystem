from django.db import models


class Reservation(models.Model):


    # STATUS_CHOICES = (
    #     ("pending", "Pending"),
    #     ("confirmed", "Confirmed"),
    #     ("checked_in", "Checked In"),
    #     ("checked_out", "Checked Out"),
    #     ("cancelled", "Cancelled"),
    # )

    STATUS_CHOICES = (
    ("reserved", "Reserved"),
    ("checked_in", "Checked In"),
    ("checked_out", "Checked Out"),
    ("cancelled", "Cancelled"),
    )
    payment_status = models.CharField(
    max_length=20,
    choices=(
        ("unpaid", "Unpaid"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    ),
    default="unpaid"
    )



    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    guest = models.ForeignKey(
        "guests.Guest",
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    check_in = models.DateField()

    check_out = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="reserved"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.guest} - Room {self.room.room_number}"