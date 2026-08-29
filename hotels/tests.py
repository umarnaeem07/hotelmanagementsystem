from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from hotels.models import Hotel
from staff.models import Staff


class HotelCreationTests(TestCase):
    def test_owner_can_create_hotel_profile(self):
        user = User.objects.create_user(
            username='hotel_owner',
            email='owner@example.com',
            password='TestPass123!'
        )

        client = APIClient()
        client.force_authenticate(user=user)

        payload = {
            'name': 'Harbor View Hotel',
            'address': '123 Ocean Drive',
            'phone': '1234567890',
            'email': 'hello@harborview.example',
            'description': 'A welcoming seaside hotel.'
        }

        response = client.post('/api/hotel/', payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Hotel.objects.filter(owner=user).exists())
        self.assertTrue(Staff.objects.filter(user=user, hotel=user.hotel, role='owner').exists())
