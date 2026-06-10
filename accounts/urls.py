from django.urls import path
from .views import LoginAPIView, MeAPIView, SignupAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("signup/",SignupAPIView.as_view(),name="signup"),
    path("login/",LoginAPIView.as_view(),name="login"),
    path("refresh/",TokenRefreshView.as_view(),name="refresh"),
    path("me/",MeAPIView.as_view(),name="me"),
    path("logout/", LogoutAPIView.as_view(), name="logout")

]
