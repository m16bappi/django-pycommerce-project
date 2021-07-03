from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from carts.models import Cart, Cart_Item
from carts.views import _get_cart_id

def cart_items_count(request):
    try:
        if request.user.is_authenticated:
            return dict(cart_items_count=Cart_Item.objects.filter(user=request.user).count())
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            return dict(cart_items_count=cart.cart_items.count())
    except ObjectDoesNotExist:
        return dict(cart_items_count=0)
