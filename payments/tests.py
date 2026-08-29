from decimal import Decimal

from django.test import TestCase
from rest_framework import serializers
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import User
from guests.models import Guest
from hotels.models import Hotel
from invoices.models import Invoice
from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.views import PaymentListCreateAPIView
from reservations.models import Reservation
from rooms.models import Room
from settings_app.models import HotelSetting


class PaymentFlowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner1",
            email="owner@example.com",
            password="pass1234",
        )
        self.hotel = Hotel.objects.create(
            owner=self.owner,
            name="Test Hotel",
            address="123 Main St",
            phone="123456789",
            email="hotel@example.com",
        )
        HotelSetting.objects.create(
            hotel=self.hotel,
            check_in_time="14:00:00",
            check_out_time="12:00:00",
            currency="PKR",
            timezone="Asia/Karachi",
            tax_percentage=Decimal("5.00"),
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            floor=1,
            room_type="standard",
            capacity=2,
            price_per_night=Decimal("100.00"),
        )
        self.guest = Guest.objects.create(
            hotel=self.hotel,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="987654321",
        )
        self.reservation = Reservation.objects.create(
            hotel=self.hotel,
            guest=self.guest,
            room=self.room,
            check_in="2026-08-20",
            check_out="2026-08-22",
            total_amount=Decimal("200.00"),
            status="reserved",
        )
        self.invoice = Invoice.objects.create(
            reservation=self.reservation,
            invoice_type="room",
            invoice_number="ROOM-1",
            subtotal=Decimal("200.00"),
            tax_amount=Decimal("10.00"),
            total_amount=Decimal("210.00"),
            payment_status="unpaid",
        )

    def test_payment_serializer_rejects_amount_over_remaining_balance(self):
        serializer = PaymentSerializer(
            data={
                "invoice": self.invoice.id,
                "amount": Decimal("300.00"),
                "payment_method": "cash",
                "transaction_reference": "TXN-001",
                "notes": "Too much",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_partial_payment_marks_invoice_and_reservation_as_partial(self):
        factory = APIRequestFactory()
        payload = {
            "invoice": self.invoice.id,
            "amount": Decimal("100.00"),
            "payment_method": "cash",
            "transaction_reference": "TXN-Partial",
            "notes": "First installment",
        }
        request = factory.post("/api/payments/", payload, format="json")
        force_authenticate(request, user=self.owner)

        response = PaymentListCreateAPIView.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.invoice.refresh_from_db()
        self.reservation.refresh_from_db()
        self.assertEqual(self.invoice.payment_status, "partial")
        self.assertEqual(self.reservation.payment_status, "partial")

    def test_full_payment_marks_invoice_and_reservation_as_paid(self):
        factory = APIRequestFactory()
        payload = {
            "invoice": self.invoice.id,
            "amount": Decimal("210.00"),
            "payment_method": "card",
            "transaction_reference": "TXN-Full",
            "notes": "Full settlement",
        }
        request = factory.post("/api/payments/", payload, format="json")
        force_authenticate(request, user=self.owner)

        response = PaymentListCreateAPIView.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.invoice.refresh_from_db()
        self.reservation.refresh_from_db()
        self.assertEqual(self.invoice.payment_status, "paid")
        self.assertEqual(self.reservation.payment_status, "paid")
