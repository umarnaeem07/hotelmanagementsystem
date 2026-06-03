from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import HousekeepingTask
from .serializers import HousekeepingTaskSerializer


class HousekeepingTaskViewSet(ModelViewSet):

    serializer_class = HousekeepingTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return HousekeepingTask.objects.filter(
            hotel=self.request.user.hotel
        )

    def perform_create(self, serializer):

        serializer.save(
            hotel=self.request.user.hotel
        )