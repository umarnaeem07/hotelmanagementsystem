from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Room
from .serializers import RoomSerializer


class RoomListCreateAPIView(APIView):
        
    permission_classes = [IsAuthenticated]

    def get(self, request):

        rooms = Room.objects.filter(
            hotel=request.user.hotel
        )

        serializer = RoomSerializer(
            rooms,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = RoomSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            hotel=request.user.hotel
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
class RoomDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):

        return Room.objects.get(
            pk=pk,
            hotel=request.user.hotel
        )

    def get(self, request, pk):

        room = self.get_object(
            request,
            pk
        )

        serializer = RoomSerializer(room)

        return Response(serializer.data)

    def put(self, request, pk):

        room = self.get_object(
            request,
            pk
        )

        serializer = RoomSerializer(
            room,
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):

        room = self.get_object(
            request,
            pk
        )

        room.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )