from django.urls import path
from .views import HotelAPIView

urlpatterns = [
    path(
        "hotel/",
        HotelAPIView.as_view(),
        name="hotel"
    ),
]