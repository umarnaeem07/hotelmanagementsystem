from django.conf import settings
from django.db import models

import accounts


class Hotel(models.Model):

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hotel"
    )

    name = models.CharField(
        max_length=255
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} ({self.owner.username})"