from django.urls import path

from .views import (
    CreateInvoiceAPIView,
    GenerateAdditionalInvoiceAPIView,
    InvoiceDetailAPIView,
)

urlpatterns = [

    path(
        "reservations/<int:reservation_id>/invoice/",
        CreateInvoiceAPIView.as_view(),
        name="create-invoice"
    ),

    path(
        "invoices/<int:pk>/",
        InvoiceDetailAPIView.as_view(),
        name="invoice-detail"
    ),
    path(
    "generate-additional/<int:reservation_id>/",
    GenerateAdditionalInvoiceAPIView.as_view(),
    name="generate-additional-invoice"
),
]