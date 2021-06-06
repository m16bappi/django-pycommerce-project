from django.contrib import admin
from .models import Products


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price',
                    'stock', 'category', 'is_available']
    prepopulated_fields = {'slug': ['product_name']}


admin.site.register(Products, ProductAdmin)
