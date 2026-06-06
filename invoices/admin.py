from django.contrib import admin
from .models import Invoice
# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "reservation", "total_amount", "issued_at")
    search_fields = ("invoice_number", "reservation__id")
    list_filter = ("issued_at",)
register = admin.site.register(Invoice, InvoiceAdmin)