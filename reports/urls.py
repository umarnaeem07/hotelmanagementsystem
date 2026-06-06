
from django.urls import path

from .views import (
    RevenueReportAPIView,
    OccupancyReportAPIView,
    ReservationReportAPIView,
)

urlpatterns = [

    path(
        "reports/revenue/",
        RevenueReportAPIView.as_view()
    ),

    path(
        "reports/occupancy/",
        OccupancyReportAPIView.as_view()
    ),

    path(
        "reports/reservations/",
        ReservationReportAPIView.as_view()
    ),
]