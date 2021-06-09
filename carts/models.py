from django.db import models
from store.models import Products


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return self.cart_id


class Cart_Item(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-product']
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'

    def __str__(self):
        return self.product.product_name
