from django.db import models
from customers.models import Customer
from inventory.models import Product


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('draft','Draft'),
        ('sent','Sent'),
        ('paid','Paid'),
        ('cancelled','Cancelled')
    ]

    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(
                    Customer,
                    on_delete=models.PROTECT,
                    related_name= 'invoices'

                    )
    
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issue_date     = models.DateField(auto_now_add=True)
    due_date       = models.DateField(null=True, blank=True)
    notes          = models.TextField(blank=True, null=True)

    discount       = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_percent    = models.DecimalField(max_digits=5, decimal_places=2, default=18)  # GST

    
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.invoice_number}-{self.customer.name}"
    
    def calculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items.all())

        # Step 2: Calculate discount
        self.discount_amount = (self.subtotal * self.discount) / 100

        # Step 3: Taxable amount after discount
        taxable              = self.subtotal - self.discount_amount

        # Step 4: Tax on the taxable amount
        self.tax_amount      = (taxable * self.tax_percent) / 100

        # Step 5: Grand total
        self.grand_total     = taxable + self.tax_amount

        # Step 6: Save only these fields (efficient — doesn't rewrite entire row)
        self.save(update_fields=['subtotal', 'discount_amount', 'tax_amount', 'grand_total'])


class InvoiceItem(models.Model):
    invoice    = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='invoice_items')
    quantity   = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"
    
    @property
    def line_total(self):
        return  self.quantity * self.unit_price
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.calculate_totals()

    def delete(self,*args, **kwargs):
        invoice = self.invoice
        super().delete(*args, **kwargs)
        invoice.calculate_totals()
        
