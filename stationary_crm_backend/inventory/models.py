from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField( max_length=200,unique=True)
    description = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(  auto_now_add=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Categories" 

class Product(models.Model):

    category = models.ForeignKey(
                Category,
                on_delete=models.SET_NULL,
                null=True,
                related_name='products'
    )

    product_name  =  models.CharField( max_length=200)
    description = models.TextField( blank=True, null=True)
    product_code = models.CharField(max_length=50, unique=True) 
    unit_price   = models.DecimalField(max_digits=10, decimal_places=2) 
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} (product_code{self.product_code})"
    
class StockRecord(models.Model):

    product_stock = models.OneToOneField(
                     Product, 
                     on_delete=models.CASCADE,
                     related_name = 'stock')
    
    quantity = models.PositiveIntegerField(default=0)
    minimum_qty = models.PositiveIntegerField(default=5)
    last_restocked   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_stock.product_name} - stock : {self.quantity}"
    
    @property
    def is_low_stock(self):
        return self.quantity<=self.minimum_qty

