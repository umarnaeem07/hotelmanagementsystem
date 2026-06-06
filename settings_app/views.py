from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import HotelSetting
from .serializers import HotelSettingSerializer


class HotelSettingAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            settings = (
                request.user
                .hotel
                .settings
            )

            serializer = HotelSettingSerializer(
                settings
            )

            return Response(
                serializer.data
            )

        except HotelSetting.DoesNotExist:

            return Response(
                {
                    "message":
                    "Settings not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):

        hotel = request.user.hotel

        if hasattr(hotel, "settings"):

            return Response(
                {
                    "message":
                    "Settings already exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HotelSettingSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            hotel=hotel
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):

        settings = (
            request.user.hotel.settings
        )

        serializer = HotelSettingSerializer(
            settings,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data
        )