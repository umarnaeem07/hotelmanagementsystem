from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Guest
from .serializers import GuestSerializer
from staff.permissions import IsReceptionistOrAbove
from activity_logs.services import log_activity



class GuestListCreateAPIView(APIView):
    
    permission_classes = [IsAuthenticated, IsReceptionistOrAbove]

    def get(self, request):

        guests = Guest.objects.filter(
            hotel=request.user.hotel
        )

        serializer = GuestSerializer(
            guests,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        

        serializer = GuestSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        guest  = serializer.save(
            hotel=request.user.hotel
        )
        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="created",
            object_type="Guest",
            object_id=guest.id,
            description=(
                f"Guest {guest.first_name} "
                f"{guest.last_name} created"
            )
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class GuestDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsReceptionistOrAbove]

    def get_object(self, request, pk):

        return Guest.objects.get(
            pk=pk,
            hotel=request.user.hotel
        )

    def get(self, request, pk):

        guest = self.get_object(
            request,
            pk
        )

        serializer = GuestSerializer(
            guest
        )

        return Response(serializer.data)

    def put(self, request, pk):

        guest = self.get_object(
            request,
            pk
        )

        serializer = GuestSerializer(
            guest,
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()
        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="updated",
            object_type="Guest",
            object_id=guest.id,
            description=(
                f"Guest {guest.first_name} "
                f"{guest.last_name} updated"
            )
        )

        return Response(serializer.data)

    def delete(self, request, pk):

        guest = self.get_object(
            request,
            pk
        )
        guest_name = (
            f"{guest.first_name} "
            f"{guest.last_name}"
        )

        guest.delete()

        log_activity(
            hotel=request.user.hotel,
            user=request.user,
            action="deleted",
            object_type="Guest",
            object_id=guest.id,
            description=(
                f"Guest {guest_name} deleted"
            )
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )