from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import StaffInvitation ,Staff
from .serializers import StaffInvitationSerializer, AcceptInvitationSerializer
from accounts.models import User
from django.core.mail import send_mail

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
        # Create invitation link
        invite_link = (
            f"{settings.FRONTEND_URL}/"
            f"accept-invitation/{invitation.token}"
        )
        # Send email
        send_mail(
            subject="Hotel Staff Invitation",
            message=(
                f"You have been invited to join "
                f"{request.user.hotel.name}.\n\n"
                f"Role: {invitation.role}\n\n"
                f"Accept your invitation here:\n"
                f"{invite_link}"
            ),
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
            recipient_list=[invitation.email],
            fail_silently=False,
        )

        return Response(
            StaffInvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED
        )
class AcceptInvitationAPIView(APIView):

    def post(self, request, token):

        try:
            invitation = (
                StaffInvitation.objects.get(
                    token=token
                )
            )

        except StaffInvitation.DoesNotExist:

            return Response(
                {
                    "message":
                    "Invalid invitation link."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if invitation.accepted:

            return Response(
                {
                    "message":
                    "Invitation already used."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = (
            AcceptInvitationSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = User.objects.create_user(
            username=serializer.validated_data[
                "username"
            ],
            email=invitation.email,
            password=serializer.validated_data[
                "password"
            ],
            role=invitation.role
        )

        Staff.objects.create(
            hotel=invitation.hotel,
            user=user,
            role=invitation.role
        )

        invitation.accepted = True
        invitation.save()

        return Response(
            {
                "message":
                "Account created successfully."
            },
            status=status.HTTP_201_CREATED
        )