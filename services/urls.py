from django.urls import path

from .views import (
    HotelServiceListCreateAPIView,
    HotelServiceDetailAPIView,
    AddReservationServiceAPIView,
    ReservationServiceListAPIView,
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
    # Reservation services
    path(
        "reservations/<int:reservation_id>/add/",
        AddReservationServiceAPIView.as_view(),
        name="reservation-add-service"
    ),

    path(
        "reservations/<int:reservation_id>/",
        ReservationServiceListAPIView.as_view(),
        name="reservation-service-list"
    ),
]