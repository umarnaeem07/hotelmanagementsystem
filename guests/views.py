from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Guest
from .serializers import GuestSerializer


class GuestViewSet(ModelViewSet):

    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Guest.objects.filter(
            hotel=self.request.user.hotel
        )

    def perform_create(self, serializer):

        serializer.save(
            hotel=self.request.user.hotel
        )