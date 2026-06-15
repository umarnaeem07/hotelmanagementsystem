from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from staff.permissions import (IsHousekeepingOrOwner)
from .models import HousekeepingTask
from .serializers import HousekeepingTaskSerializer


class HousekeepingTaskListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsHousekeepingOrOwner]

    def get(self, request):

        tasks = HousekeepingTask.objects.filter(
            hotel=request.user.hotel
        )

        serializer = HousekeepingTaskSerializer(
            tasks,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = HousekeepingTaskSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        task = serializer.save(
            hotel=request.user.hotel
        )

        return Response(
            HousekeepingTaskSerializer(task).data,
            status=status.HTTP_201_CREATED
        )
class HousekeepingTaskDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsHousekeepingOrOwner]

    def get_object(self, request, pk):

        return HousekeepingTask.objects.get(
            pk=pk,
            hotel=request.user.hotel
        )

    def get(self, request, pk):

        task = self.get_object(
            request,
            pk
        )

        serializer = HousekeepingTaskSerializer(
            task
        )

        return Response(serializer.data)

    def put(self, request, pk):

        task = self.get_object(
            request,
            pk
        )

        serializer = HousekeepingTaskSerializer(
            task,
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):

        task = self.get_object(
            request,
            pk
        )

        task.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )