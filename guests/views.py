from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Guest
from .serializers import GuestSerializer


class GuestListCreateAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

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

        serializer.save(
            hotel=request.user.hotel
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class GuestDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

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

        return Response(serializer.data)

    def delete(self, request, pk):

        guest = self.get_object(
            request,
            pk
        )

        guest.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )