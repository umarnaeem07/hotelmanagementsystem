from django.db import models


class Invoice(models.Model):

    reservation = models.OneToOneField(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="invoice"
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    issued_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number