from django.urls import path

from .views import (
    CheckInEligibilityAPIView,
    CheckoutEligibilityAPIView
)

urlpatterns = [
    path(
        "check-in-eligibility/",
        CheckInEligibilityAPIView.as_view()
    ),
    path(
        "checkout-eligibility/",
        CheckoutEligibilityAPIView.as_view()
    ),
]