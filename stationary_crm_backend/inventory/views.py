from django.shortcuts import render
from .serializers import CategorySerializer,StockRecordSerializer,ProductSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, StockRecord



@api_view(['GET','POST'])
def category_list (request):

    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','POST'])
def product_list(request):

    if request.method == 'GET':

        category_id = request.query_params.get('category',None) 
        products = Product.objects.filter(is_active = True)

        if category_id is not None:
            products = Product.objects.filter(category_id = category_id)

        
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)
    
    if request.method =='POST':
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid:
            product = serializer.save()
                                                                    
            StockRecord.objects.create(product=product, quantity=0) # Auto create a stock record when a new product is added
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def product_details(request,pk):

    try:
        
        product = Product.objects.get(pk=pk)    
    except Product.DoesNotExist:
        return Response({"error":"Product does not exist"},status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.is_active = False
        product.save()
        return Response({"message": "Product deactivated"}) 

@api_view(['PUT'])
def stock_update(request,pk):

    try:
        stock = StockRecord.objects.get(product_stock_id = pk)
    except StockRecord.DoesNotExist:
        return Response({"error": "Stock record not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StockRecordSerializer(stock , data= request.data , partial = True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

