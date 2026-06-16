from rest_framework import serializers

from .models import Payment


class PaymentSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Payment

        fields = (
            "id",
            "invoice",
            "amount",
            "payment_method",
            "transaction_reference",
            "notes",
            "received_by",
            "paid_at",
        )

        read_only_fields = (
            "received_by",
            "paid_at",
        )

    def validate(self, attrs):

        invoice = attrs["invoice"]
        amount = attrs["amount"]

        already_paid = sum(
            payment.amount
            for payment in invoice.payments.all()
        )

        remaining = (
            invoice.total_amount -
            already_paid
        )

        if amount > remaining:

            raise serializers.ValidationError(
                "Payment exceeds remaining balance."
            )

        return attrs