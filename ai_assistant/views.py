from rest_framework.views import APIView
from rest_framework.response import Response
from .extractor import (
    extract_reservation_id
)
from rest_framework.views import APIView
from rest_framework.response import Response

from .router.chat_router import chat_router


class ChatAPIView(APIView):

    def post(self, request):

        question = request.data.get("question")

        result = chat_router.invoke(
            {
                "question": question,
                "hotel_id": request.user.hotel.id,
            }
        )

        return Response(
            {
                "answer": result["answer"],
                "intent": result["intent"],
                "raw_result": result["result"],
            }
            )