from django.core.exceptions import ObjectDoesNotExist
from carts.models import Cart
from carts.views import _get_cart_id

def cart_items_count(request):
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        return dict(cart_items_count=cart.cart_items.count())
    except ObjectDoesNotExist:
        return dict(cart_items_count=0)
