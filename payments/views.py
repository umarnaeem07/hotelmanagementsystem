from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import (
    get_object_or_404
)

from .models import Payment
from .serializers import PaymentSerializer

class PaymentListCreateAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        payments = Payment.objects.filter(
            reservation__hotel=
            request.user.hotel
        )

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = PaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
class PaymentDetailAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, pk):

        payment = get_object_or_404(
            Payment,
            pk=pk,
            reservation__hotel=
            request.user.hotel
        )

        serializer = PaymentSerializer(
            payment
        )

        return Response(
            serializer.data
        )
