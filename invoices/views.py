from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from reservations.models import Reservation

from .models import Invoice
from .serializers import InvoiceSerializer

class CreateInvoiceAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):

        reservation = get_object_or_404(
            Reservation,
            pk=reservation_id,
            hotel=request.user.hotel
        )

        if hasattr(reservation, "invoice"):

            return Response(
                {
                    "message":
                    "Invoice already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        subtotal = reservation.total_amount

        tax_percentage = (
            request.user.hotel
            .settings
            .tax_percentage
        )

        tax_amount = (
            subtotal * tax_percentage
        ) / 100

        total_amount = (
            subtotal + tax_amount
        )

        invoice = Invoice.objects.create(
            reservation=reservation,
            invoice_number=f"INV-{reservation.id}",
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount
        )

        serializer = InvoiceSerializer(
            invoice
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
class InvoiceDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        invoice = get_object_or_404(
            Invoice,
            pk=pk,
            reservation__hotel=
            request.user.hotel
        )

        serializer = InvoiceSerializer(
            invoice
        )

        return Response(
            serializer.data
        )
    