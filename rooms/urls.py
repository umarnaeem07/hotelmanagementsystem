from django.urls import path

from .views import (
    RoomListCreateAPIView,
    RoomDetailAPIView,
)

urlpatterns = [
    path(
        "rooms/",
        RoomListCreateAPIView.as_view(),
        name="room-list-create"
    ),

    path(
        "rooms/<int:pk>/",
        RoomDetailAPIView.as_view(),
        name="room-detail"
    ),
]