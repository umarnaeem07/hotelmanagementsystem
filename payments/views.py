from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import (get_object_or_404)
from staff.permissions import IsCashierOrOwner

from .models import Payment
from .serializers import PaymentSerializer

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

        invoice = payment.invoice

        total_paid = sum(
            p.amount
            for p in invoice.payments.all()
        )

        if total_paid >= invoice.total_amount:
            invoice.payment_status = "paid"
            invoice.save()

            if invoice.invoice_type == "room":
                reservation = invoice.reservation
                reservation.payment_status = "paid"
                reservation.save()

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
