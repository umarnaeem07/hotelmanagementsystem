from django.db import models


class Invoice(models.Model):

    INVOICE_TYPES = (
        ("room", "Room Invoice"),
        ("additional", "Additional Charges"),
    )

    PAYMENT_STATUS = (
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
    )

    reservation = models.ForeignKey(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    invoice_type = models.CharField(
        max_length=20,
        choices=INVOICE_TYPES
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

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="unpaid"
    )

    issued_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.invoice_number} "
            f"({self.invoice_type})"
        )