from django.db import models


class HousekeepingTask(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="housekeeping_tasks"
    )

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="housekeeping_tasks"
    )

    title = models.CharField(
        max_length=255
    )

    notes = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.room.room_number} - {self.title}"