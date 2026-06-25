# chat/models.py

from django.db import models


class ChatSession(models.Model):

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class ChatMessage(models.Model):

    ROLE_CHOICES = (
        ("user", "User"),
        ("assistant", "Assistant"),
    )

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )