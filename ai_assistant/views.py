from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.models import ChatSession, ChatMessage
from chat.services import (
    save_user_message,
    save_assistant_message,
)

from .router.chat_router import chat_router


class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hotel = getattr(request.user, 'hotel', None)
        if not hotel:
            return Response({
                'session_id': None,
                'messages': [],
            })

        session, _ = ChatSession.objects.get_or_create(
            user=request.user,
            hotel=hotel,
        )

        messages = session.messages.order_by('created_at')
        serialized = [
            {
                'id': message.id,
                'role': message.role,
                'content': message.content,
                'created_at': message.created_at.isoformat(),
            }
            for message in messages
        ]

        return Response({
            'session_id': session.id,
            'messages': serialized,
        })

    def post(self, request):

        question = request.data.get(
            "question"
        )

        if not question or not str(question).strip():
            return Response(
                {"message": "Question is required."},
                status=400,
            )

        hotel = getattr(request.user, 'hotel', None)
        if not hotel:
            return Response(
                {"message": "Please create your hotel profile before using the AI assistant."},
                status=400,
            )

        session, created = (
            ChatSession.objects.get_or_create(
                user=request.user,
                hotel=hotel
            )
        )

        save_user_message(
            session,
            question
        )

        result = chat_router.invoke(
            {
                "session_id": session.id,
                "question": question,
                "hotel_id": hotel.id,
            }
        )

        save_assistant_message(
            session,
            result["answer"]
        )

        return Response(
            {
                "answer": result["answer"],
                "intent": result["intent"],
                "raw_result": result["result"],
            }
        )