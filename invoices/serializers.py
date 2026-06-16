from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Invoice

        fields = (
            "id",
            "reservation",
            "invoice_type",
            "invoice_number",
            "subtotal",
            "tax_amount",
            "total_amount",
            "payment_status",
            "issued_at",
        )

        read_only_fields = (
            "invoice_type",
            "invoice_number",
            "subtotal",
            "tax_amount",
            "total_amount",
            "payment_status",
            "issued_at",
        )