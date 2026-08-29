from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from guests.models import Guest
from hotels.models import Hotel
from reservations.models import Reservation
from rooms.models import Room


class ReservationRoomLifecycleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='hotel_owner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.hotel = Hotel.objects.create(
            owner=self.user,
            name='Harbor View',
            address='123 Main St',
            phone='1234567890',
            email='hotel@example.com',
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number='101',
            floor=1,
            room_type='standard',
            capacity=2,
            price_per_night=120,
            status='available',
        )
        self.guest = Guest.objects.create(
            hotel=self.hotel,
            first_name='Alice',
            last_name='Guest',
            email='alice@example.com',
            phone='9876543210',
        )

    def test_room_status_moves_from_reserved_to_occupied_to_cleaning(self):
        reservation = Reservation.objects.create(
            hotel=self.hotel,
            guest=self.guest,
            room=self.room,
            check_in=timezone.now().date(),
            check_out=(timezone.now() + timezone.timedelta(days=2)).date(),
            status='reserved',
            total_amount=240,
        )

        self.room.status = 'reserved'
        self.room.save(update_fields=['status'])
        self.room.refresh_from_db()
        self.assertEqual(self.room.status, 'reserved')

        reservation.status = 'checked_in'
        reservation.save()
        self.room.status = 'occupied'
        self.room.save(update_fields=['status'])
        self.room.refresh_from_db()
        self.assertEqual(self.room.status, 'occupied')

        reservation.status = 'checked_out'
        reservation.save()
        self.room.status = 'cleaning'
        self.room.save(update_fields=['status'])
        self.room.refresh_from_db()
        self.assertEqual(self.room.status, 'cleaning')
