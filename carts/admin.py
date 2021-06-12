from django.contrib import admin
from .models import Cart, Cart_Item

class CartAmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'is_active']

admin.site.register(Cart, CartAmin)
admin.site.register(Cart_Item, CartItemAdmin)
