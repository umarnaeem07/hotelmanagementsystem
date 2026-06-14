from django.db import models


class Staff(models.Model):

    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("manager", "Manager"),
        ("receptionist", "Receptionist"),
        ("housekeeping", "Housekeeping"),
        ("cashier", "Cashier"),
    )

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="staff_members"
    )

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"

import uuid

from django.db import models


class StaffInvitation(models.Model):

    ROLE_CHOICES = (
        ("manager", "Manager"),
        ("receptionist", "Receptionist"),
        ("housekeeping", "Housekeeping"),
        ("cashier", "Cashier"),
    )

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="invitations"
    )

    email = models.EmailField()

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    accepted = models.BooleanField(
        default=False
    )

    invited_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="sent_invitations"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hotel", "email"],
                condition=models.Q(accepted=False),
                name="unique_pending_invitation"
            )
        ]

    def __str__(self):
        return f"{self.email} - {self.role}"