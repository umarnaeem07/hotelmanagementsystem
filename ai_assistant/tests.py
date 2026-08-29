from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from chat.models import ChatSession, ChatMessage
from hotels.models import Hotel


class ChatHistoryTests(TestCase):
    def test_returns_previous_chat_messages_for_logged_in_user(self):
        user = User.objects.create_user(
            username='assistant_user',
            email='assistant@example.com',
            password='TestPass123!'
        )
        hotel = Hotel.objects.create(
            owner=user,
            name='Harbor View',
            address='123 Main Street',
            phone='1234567890',
            email='hello@harborview.example',
        )
        session = ChatSession.objects.create(user=user, hotel=hotel)
        ChatMessage.objects.create(session=session, role='user', content='Check occupancy')
        ChatMessage.objects.create(session=session, role='assistant', content='Occupancy is 86%')

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/api/chat/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['messages']), 2)
        self.assertEqual(response.data['messages'][0]['role'], 'user')
        self.assertEqual(response.data['messages'][1]['role'], 'assistant')

    def test_returns_clear_error_when_user_has_no_hotel_profile(self):
        user = User.objects.create_user(
            username='hotelless_user',
            email='hotelless@example.com',
            password='TestPass123!'
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post('/api/chat/', {'question': 'What is the occupancy today?'}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('hotel profile', response.data['message'])
