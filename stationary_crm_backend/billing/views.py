from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, CreateInvoiceSerializer
from customers.models import Customer
from inventory.models import Product
import datetime

def generate_invoice_number():
    last = Invoice.objects.order_by('id').last
    if not last:
        return 'INV-0001'
    last_number = int(last.invoice_number.split('-')[1])
    return f'INV - {str(last_number + 1).zfill(4)}'


@api_view(['GET','POST'])
def invoice_list(request):
    if request.method ==  'GET':
        invoices = Invoice.objects.all().select_related('customer')
        serializer = InvoiceSerializer(invoices,many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CreateInvoiceSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    data = serializer.validated_data

    try:
        customer = Customer.objects.get(pk=data['customer'])
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)   

    with transaction.atomic():

        # Step 1: Create the invoice
        invoice = Invoice.objects.create(
            invoice_number = generate_invoice_number(),
            customer = customer,
            discount       = data.get('discount', 0),
            tax_percent    = data.get('tax_percent', 18),
            due_date       = data.get('due_date', None),
            notes          = data.get('notes', ''),
        ) 

        # Step 2: Create each invoice item
        for item_data in data['items']:
            try:
                product = Product.objects.get(pk=data['items'])
            except product.DoesNotExist:
                raise Exception(f"Product id {item_data['product']} not found")

            InvoiceItem.objects.create(
                invoice = invoice,
                product = product,
                quantity = item_data['quantity'],
                unit_price = product.unit_price,  # snapshot current price
            )
                # ↑ InvoiceItem.save() auto-triggers calculate_totals()

    # Return the created invoice with all details
    response_serializer = InvoiceSerializer(invoice)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)    


@api_view(['GET','PUT','DELETE'])
def invoice_detail(request,pk):

    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method ==  'GET':
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        allowed_fields = ['status', 'notes', 'due_date']
        data = {k: v for k, v in request.data.items() if k in allowed_fields}
        serializer = InvoiceSerializer(invoice,data=data,partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if invoice.status == 'paid':
            return Response(
                {"error": "Cannot delete a paid invoice"},
                status=status.HTTP_400_BAD_REQUEST
            )
        invoice.delete()
        return Response({"message": "Invoice deleted"}, status=status.HTTP_204_NO_CONTENT)
