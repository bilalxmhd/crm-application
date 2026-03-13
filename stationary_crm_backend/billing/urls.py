from django.urls import path
from . import views

urlpatterns = [
    path('invoices/',          views.invoice_list,   name='invoice-list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice-detail'),
]