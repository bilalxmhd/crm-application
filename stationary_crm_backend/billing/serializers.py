from .models import Invoice,InvoiceItem
from rest_framework import serializers 

class InvoiceItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source ='product.name', read_only=True)
    line_total   = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = ['id','product','product_name','quantity','unit_price','line_total']

class InvoiceSerializer(serializers.ModelSerializer):
    items         = InvoiceItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Invoice
        fields = [ 'id', 'invoice_number', 'customer', 'customer_name',
            'status', 'issue_date', 'due_date',
            'discount', 'tax_percent',
            'subtotal', 'discount_amount', 'tax_amount', 'grand_total',
            'notes', 'items',
            'created_at']  
        read_only_fields = ['subtotal', 'discount_amount', 'tax_amount', 'grand_total']      

class CreateInvoiceSerializer(serializers.Serializer):
    """
    Special serializer for creating a full invoice with items in one API call.
    Accepts:
    {
        "customer": 1,
        "discount": 10,
        "tax_percent": 18,
        "due_date": "2026-03-01",
        "items": [
            {"product": 1, "quantity": 10},
            {"product": 2, "quantity": 3}
        ]
    }
    """
    customer    = serializers.IntegerField()
    discount    = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_percent = serializers.DecimalField(max_digits=5, decimal_places=2, default=18)
    due_date    = serializers.DateField(required=False)
    notes       = serializers.CharField(required=False, allow_blank=True)
    items       = serializers.ListField(
                      child=serializers.DictField(),
                      min_length=1  # at least 1 item required
                  )