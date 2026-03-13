from django.urls import path
from . import  views

urlpatterns = [
    path('categories/',          views.category_list,   name='category-list'),
    path('products/',            views.product_list,    name='product-list'),
    path('products/<int:pk>/',   views.product_details,  name='product-detail'),
    path('products/<int:pk>/stock/', views.stock_update, name='update-stock'),
]
