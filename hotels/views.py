from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Hotel
from .serializers import HotelSerializer


class HotelAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            hotel = request.user.hotel
            serializer = HotelSerializer(hotel)

            return Response(serializer.data)

        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):

        if hasattr(request.user, "hotel"):
            return Response(
                {"message": "Hotel already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HotelSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            owner=request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):

        hotel = request.user.hotel

        serializer = HotelSerializer(
            hotel,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(serializer.data)