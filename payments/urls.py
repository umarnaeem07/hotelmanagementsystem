from django.urls import path

from .views import (
    PaymentListCreateAPIView,
    PaymentDetailAPIView,
)

urlpatterns = [

    path(
        "payments/",
        PaymentListCreateAPIView.as_view()
    ),

    path(
        "payments/<int:pk>/",
        PaymentDetailAPIView.as_view()
    ),

]