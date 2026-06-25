from rest_framework.views import APIView
from rest_framework.response import Response

from chat.models import ChatSession
from chat.services import (
    save_user_message,
    save_assistant_message,
)

from .router.chat_router import chat_router


class ChatAPIView(APIView):

    def post(self, request):

        question = request.data.get(
            "question"
        )

        session, created = (
            ChatSession.objects.get_or_create(
                user=request.user,
                hotel=request.user.hotel
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
                "hotel_id": request.user.hotel.id,
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