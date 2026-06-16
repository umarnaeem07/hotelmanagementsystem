from django.urls import path
from .views import CheckInAPIView,CheckOutAPIView
from .views import (
    ReservationListCreateAPIView,
    ReservationDetailAPIView,
    ReservationServiceAPIView,
    ReservationServiceDetailAPIView 
)


urlpatterns = [

    path(
        "reservations/",
        ReservationListCreateAPIView.as_view(),
        name="reservation-list-create"
    ),

    path(
        "reservations/<int:pk>/",
        ReservationDetailAPIView.as_view(),
        name="reservation-detail"
    ),
    path(
        "reservations/<int:pk>/check-in/",
        CheckInAPIView.as_view(),
        name="check-in"
    ),

    path(
        "reservations/<int:pk>/check-out/",
        CheckOutAPIView.as_view(),
        name="check-out"
    ),
    path(
        "reservations/<int:reservation_id>/services/",
        ReservationServiceAPIView.as_view(),
        name="reservation-services"
    ),
    path(
        "reservations/<int:reservation_id>/services/<int:service_id>/",
        ReservationServiceDetailAPIView.as_view(),
        name="reservation-service-detail"
    ),
]