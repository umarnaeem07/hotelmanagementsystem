from django.urls import path
from .views import CheckInAPIView,CheckOutAPIView
from .views import (
    ReservationListCreateAPIView,
    ReservationDetailAPIView,
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
]