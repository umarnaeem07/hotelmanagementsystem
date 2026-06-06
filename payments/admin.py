from django.contrib import admin
from .models import Payment

# Register your models here.
# admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reservation",
        "amount",
        "payment_method",
        "paid_at",
    )

    list_filter = (
        "payment_method",
        "paid_at",
    )

    search_fields = (
        "reservation__id",
        "transaction_reference",
    )
admin.site.register(Payment, PaymentAdmin)