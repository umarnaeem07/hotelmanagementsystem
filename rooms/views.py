from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(ModelViewSet):

    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Room.objects.filter(
            hotel=self.request.user.hotel
        )

    def perform_create(self, serializer):

        serializer.save(
            hotel=self.request.user.hotel
        )