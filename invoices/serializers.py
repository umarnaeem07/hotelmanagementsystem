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
            "invoice_number",
            "subtotal",
            "tax_amount",
            "total_amount",
            "issued_at",
        )

        read_only_fields = (
            "invoice_number",
            "subtotal",
            "tax_amount",
            "total_amount",
            "issued_at",
        )