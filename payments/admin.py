from django.contrib import admin
from .models import Payment

# Register your models here.
# admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
    "id",
    "invoice",
    "amount",
    "payment_method",
    "paid_at",
)

    list_filter = (
        "payment_method",
        "paid_at",
    )

    search_fields = (
    "invoice__invoice_number",
    "transaction_reference",
)
admin.site.register(Payment, PaymentAdmin)