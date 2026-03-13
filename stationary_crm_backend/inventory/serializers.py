from rest_framework import serializers
from .models import Category,Product,StockRecord


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category,
        fields = '__all__'


class StockRecordSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()

    class Meta:
        model = StockRecord,
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    stock = StockRecordSerializer(read_only = True) # Nest stock info inside product response
    category_name = serializers.CharField(source = 'category.name',read_only = True)

    class Meta:
        model= Product,
        fields = ['id','product_name','category','category_name',
                  'description','product_code','unit_price','is_active','stock','created_at']     