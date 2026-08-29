from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import (get_object_or_404)
from staff.permissions import IsCashierOrOwner

from .models import Payment
from .serializers import PaymentSerializer
from activity_logs.services import log_activity
class PaymentListCreateAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsCashierOrOwner
    ]

    def get(self, request):

        payments = Payment.objects.filter(
        invoice__reservation__hotel=
        request.user.hotel
    )

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = PaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        # serializer.save()
        payment = serializer.save(
            received_by=request.user
        )
        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="payment_received",
            object_type="Payment",
            object_id=payment.id,
            description=(
                f"Payment of {payment.amount} "
                f"received for invoice "
                f"{payment.invoice.invoice_number}"
            )
        )

        invoice = payment.invoice

        total_paid = sum(
            p.amount
            for p in invoice.payments.all()
        )

        if total_paid <= 0:
            invoice.payment_status = "unpaid"
        elif total_paid < invoice.total_amount:
            invoice.payment_status = "partial"
        else:
            invoice.payment_status = "paid"

        invoice.save()

        if invoice.payment_status == "paid":
            log_activity(
                hotel=request.user.hotel,
                user=request.user,
                action="invoice_paid",
                object_type="Invoice",
                object_id=invoice.id,
                description=(
                    f"Invoice "
                    f"{invoice.invoice_number} "
                    f"marked as paid"
                )
            )

        if invoice.invoice_type == "room":
            reservation = invoice.reservation
            reservation.payment_status = invoice.payment_status
            reservation.save()

            if invoice.payment_status == "paid":
                log_activity(
                    hotel=request.user.hotel,
                    user=request.user,
                    action="reservation_paid",
                    object_type="Reservation",
                    object_id=reservation.id,
                    description=(
                        f"Reservation "
                        f"#{reservation.id} "
                        f"payment completed"
                    )
                )
            elif invoice.payment_status == "partial":
                log_activity(
                    hotel=request.user.hotel,
                    user=request.user,
                    action="reservation_partial_payment",
                    object_type="Reservation",
                    object_id=reservation.id,
                    description=(
                        f"Reservation "
                        f"#{reservation.id} "
                        f"received partial payment"
                    )
                )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
class PaymentDetailAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsCashierOrOwner
    ]

    def get(self, request, pk):

        payment = get_object_or_404(
            Payment,
            pk=pk,
            invoice__reservation__hotel=
            request.user.hotel
        )

        serializer = PaymentSerializer(
            payment
        )

        return Response(
            serializer.data
        )
