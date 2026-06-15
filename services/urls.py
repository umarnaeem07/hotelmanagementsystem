from django.urls import path

from .views import (
    HotelServiceListCreateAPIView,
    HotelServiceDetailAPIView,
)

urlpatterns = [

    path(
        "services/",
        HotelServiceListCreateAPIView.as_view(),
        name="service-list-create"
    ),

    path(
        "services/<int:pk>/",
        HotelServiceDetailAPIView.as_view(),
        name="service-detail"
    ),
]