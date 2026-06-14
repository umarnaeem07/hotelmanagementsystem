from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import StaffInvitation
from .serializers import StaffInvitationSerializer


class StaffInvitationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        invitations = StaffInvitation.objects.filter(
            hotel=request.user.hotel
        )

        serializer = StaffInvitationSerializer(
            invitations,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = StaffInvitationSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        invitation = serializer.save(
            hotel=request.user.hotel,
            invited_by=request.user
        )

        return Response(
            StaffInvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED
        )