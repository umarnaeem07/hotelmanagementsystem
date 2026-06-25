from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from staff.permissions import IsCashierOrOwner
from reservations.models import Reservation
from services.models import ReservationService
from .models import Invoice
from .serializers import InvoiceSerializer
from activity_logs.services import log_activity

class CreateInvoiceAPIView(APIView):

    permission_classes = [IsAuthenticated,IsCashierOrOwner]

    def post(self, request, reservation_id):


        reservation = get_object_or_404(
            Reservation,
            pk=reservation_id,
            hotel=request.user.hotel
        )

        if Invoice.objects.filter(
            reservation=reservation,
            invoice_type="room"
        ).exists():
            return Response(
                {
                    "message": "Room invoice already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------
        # Calculate room charges
        # ----------------------------
        room_total = (
            reservation.total_amount
        )

        subtotal = reservation.total_amount

        tax_percentage = (
            request.user.hotel
            .settings
            .tax_percentage
        )

        tax_amount = (
            subtotal *
            tax_percentage
        ) / 100

        total_amount = (
            subtotal +
            tax_amount
        )

        invoice = Invoice.objects.create(
                reservation=reservation,
                invoice_type="room",
                invoice_number=f"ROOM-{reservation.id}",
                subtotal=subtotal,
                tax_amount=tax_amount,
                total_amount=total_amount,
                payment_status="unpaid"
            )
        log_activity(
            
                hotel=request.user.hotel,
                user=request.user,
                action="created",
                object_type="Invoice",
                object_id=invoice.id,
                description=(
                    f"Room invoice created "
                    f"for reservation #{reservation.id}"
                )
            )
        
        

        serializer = InvoiceSerializer(
            invoice
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
class InvoiceDetailAPIView(APIView):

    permission_classes = [IsAuthenticated,IsCashierOrOwner]

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
    

class GenerateAdditionalInvoiceAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsCashierOrOwner
    ]

    def post(
        self,
        request,
        reservation_id
    ):

        reservation = get_object_or_404(
            Reservation,
            pk=reservation_id,
            hotel=request.user.hotel
        )

        # Prevent duplicate additional invoice

        if Invoice.objects.filter(
            reservation=reservation,
            invoice_type="additional"
        ).exists():

            return Response(
                {
                    "message":
                    "Additional invoice already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        services = (
            ReservationService.objects.filter(
                reservation=reservation
            )
        )

        subtotal = sum(
            service.total_price
            for service in services
        )

        if subtotal <= 0:

            return Response(
                {
                    "message":
                    "No service charges found."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        tax_percentage = (
            request.user.hotel
            .settings
            .tax_percentage
        )

        tax_amount = (
            subtotal *
            tax_percentage
        ) / 100

        total_amount = (
            subtotal +
            tax_amount
        )

        invoice = Invoice.objects.create(
            reservation=reservation,
            invoice_type="additional",
            invoice_number=
            f"ADD-{reservation.id}",

            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,

            payment_status="unpaid"
        )
        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="created",
            object_type="Invoice",
            object_id=invoice.id,
            description=(
                f"Room invoice created "
                f"for reservation #{reservation.id}"
            )
        )

        serializer = InvoiceSerializer(
            invoice
        )
        

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )