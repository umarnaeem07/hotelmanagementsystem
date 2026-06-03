from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractUser):

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ["email"]