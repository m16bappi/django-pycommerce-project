from django.urls import path

from .views import *

urlpatterns = [
    path('', CartView, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_to_cart/<int:product_id>/', remove_to_cart, name='remove_to_cart'),
    path('delete_to_Cart/<int:product_id>/', delete_to_cart, name='delete_to_cart'),
    path('checkout/', checkout, name='checkout')
]
