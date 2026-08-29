from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from staff.models import Staff
from staff.permissions import IsOwner
from .models import Hotel
from .serializers import HotelSerializer



class HotelAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            hotel = Hotel.objects.get(owner=request.user)
            serializer = HotelSerializer(hotel)

            return Response(serializer.data)

        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if Hotel.objects.filter(owner=request.user).exists():
            return Response(
                {"message": "Hotel already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hotel = serializer.save(owner=request.user)
        Staff.objects.get_or_create(
            user=request.user,
            defaults={
                "hotel": hotel,
                "role": "owner",
            },
        )

        return Response(
            HotelSerializer(hotel).data,
            status=status.HTTP_201_CREATED,
        )

    def put(self, request):
        try:
            hotel = Hotel.objects.get(owner=request.user)
        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel profile not found. Please set up your hotel first."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = HotelSerializer(hotel, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)