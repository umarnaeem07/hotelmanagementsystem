from rest_framework import serializers

from .models import Payment


class PaymentSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Payment

        fields = (
            "id",
            "reservation",
            "amount",
            "payment_method",
            "transaction_reference",
            "notes",
            "paid_at",
        )

        read_only_fields = (
            "paid_at",
        )
        def validate(self, attrs):

            reservation = attrs["reservation"]

            amount = attrs["amount"]

            already_paid = sum(
                payment.amount
                for payment in reservation.payments.all()
            )

            remaining = (
                reservation.total_amount -
                already_paid
            )

            if amount > remaining:

                raise serializers.ValidationError(
                    "Payment exceeds remaining balance."
                )

            return attrs