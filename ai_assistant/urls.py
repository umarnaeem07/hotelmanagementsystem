from django.urls import path

from .views import (
    CheckInEligibilityAPIView
)

urlpatterns = [
    path(
        "check-in-eligibility/",
        CheckInEligibilityAPIView.as_view()
    ),
]