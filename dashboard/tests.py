from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class DashboardHotelSetupTests(TestCase):
    def test_dashboard_requires_hotel_profile(self):
        user = User.objects.create_user(
            username='newowner',
            email='newowner@example.com',
            password='TestPass123!'
        )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = self.client.get(
            reverse('dashboard'),
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('Hotel profile not found', response.json()['message'])
