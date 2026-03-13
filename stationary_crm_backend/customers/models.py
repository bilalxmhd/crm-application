from django.db import models

# Create your models here.
class Customer(models.Model):
    
    Customer_type_choices = [
        ('retail','Retail'),
        ('wholesale','Wholesale')
    ]

    name  = models.CharField(max_length=200)
    phone = models.CharField(max_length=15 , unique= True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    customer_type = models.CharField(
                        max_length=20,
                        choices= Customer_type_choices,
                        default='retail'
                    )
    
    created_at    = models.DateTimeField(auto_now_add=True)  
    updated_at    = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return f"{self.name} ({self.phone})"
    
    class Meta:
        ordering = ['-created_at']