from django.contrib import admin
from .models import Category, Product, StockRecord

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['product_name', 'product_code', 'category', 'unit_price', 'is_active']
    search_fields = ['product_name', 'product_code']
    list_filter   = ['category', 'is_active']

@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ['product_stock', 'quantity', 'minimum_qty', 'is_low_stock']