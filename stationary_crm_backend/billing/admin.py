from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model  = InvoiceItem
    extra  = 1  # shows 1 empty row to add items

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display  = ['invoice_number', 'customer', 'status', 'issue_date', 'grand_total']
    list_filter   = ['status']
    search_fields = ['invoice_number', 'customer__name']
    inlines       = [InvoiceItemInline]  # show items inside the invoice page