from rest_framework.views import APIView
from rest_framework.response import Response

from .graph import graph

class CheckInEligibilityAPIView(
    APIView
):

    def post(self, request):

        reservation_id = request.data.get(
            "reservation_id"
        )

        result = graph.invoke(
            {
                "reservation_id":
                reservation_id
            }
        )

        return Response(result)