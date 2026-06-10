from django.urls import path

from .views import (
    GuestListCreateAPIView,
    GuestDetailAPIView,
)

urlpatterns = [
    path(
        "guests/",
        GuestListCreateAPIView.as_view(),
        name="guest-list-create"
    ),

    path(
        "guests/<int:pk>/",
        GuestDetailAPIView.as_view(),
        name="guest-detail"
    ),
]