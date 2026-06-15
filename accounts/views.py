from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.serializers import SignupSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class SignupAPIView(APIView):

    def post(self, request):

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Account created",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,    
                }
            },
            status=status.HTTP_201_CREATED
        )
    
class LoginAPIView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),

            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
            }
        })
class MeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)
    
class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data.get("refresh")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "success": True,
                    "message": "Logged out successfully."
                },
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
from django.contrib.auth import get_user_model
from .models import PasswordResetToken
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()


class ForgotPasswordAPIView(APIView):

    def post(self, request):

        email = request.data.get("email")

        try:
            user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            return Response(
                {
                    "message":
                    "No account found with this email."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        reset_token = PasswordResetToken.objects.create(
            user=user
        )

        reset_link = (
            f"{settings.FRONTEND_URL}/"
            f"reset-password/{reset_token.token}"
        )

        send_mail(
            subject="Reset Your Password",
            message=(
                f"Hello {user.username},\n\n"
                f"Click the link below to reset your password:\n\n"
                f"{reset_link}\n\n"
                f"This link will expire in 1 hour."
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {
                "success": True,
                "message":
                "Password reset email sent."
            }
        )
class ResetPasswordAPIView(APIView):

    def post(
        self,
        request,
        token
    ):

        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                is_used=False
            )

        except PasswordResetToken.DoesNotExist:
            return Response(
                {
                    "message":
                    "Invalid reset token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if reset_token.is_expired():

            return Response(
                {
                    "message":
                    "Reset link has expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        password = request.data.get(
            "password"
        )

        if not password:
            return Response(
                {
                    "message":
                    "Password is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = reset_token.user
        user.set_password(password)
        user.save()

        reset_token.is_used = True
        reset_token.save()

        return Response(
            {
                "success": True,
                "message":
                "Password reset successfully."
            }
        )