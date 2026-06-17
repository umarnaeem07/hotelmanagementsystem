from rest_framework.views import APIView
from rest_framework.response import Response
from .extractor import (
    extract_reservation_id
)
from .graph import graph
from .responder import (
    generate_answer
)

from .graphs.checkout_graph import graph
class CheckInEligibilityAPIView(
    APIView
):

    def post(self, request):

        # reservation_id = request.data.get(
        #     "reservation_id"
        # )
        question = request.data.get(
                    "question"
                )

        reservation_id = (
                    extract_reservation_id(
                        question))

        result = graph.invoke(
            {
                "reservation_id":
                reservation_id
            }
        )

        answer = generate_answer(
            question,
            result
        )

        return Response(answer)

class CheckoutEligibilityAPIView(
    APIView
):

    def post(self, request):

        reservation_id = request.data.get(
            "reservation_id"
        )

        result = graph.invoke(
            {
                "reservation_id":
                reservation_id,

                "steps": []
            }
        )

        return Response(result)