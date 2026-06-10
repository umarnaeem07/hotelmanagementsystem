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
