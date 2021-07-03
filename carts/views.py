from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Products, Variation
from .models import Cart, Cart_Item


def _get_cart_id(request):
    key = request.session.session_key
    if not key:
        key = request.session.create()
    return key


def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)

    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except ObjectDoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except ObjectDoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))
    cart.save()

    is_cart_item_exists = Cart_Item.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = Cart_Item.objects.filter(product=product, cart=cart)

        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = Cart_Item.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = Cart_Item.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()

    else:
        cart_item = Cart_Item.objects.create(product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()

    return redirect('cart')


def remove_to_cart(request, product_id, cart_item_id):
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        item = Cart_Item.objects.get(cart=cart, product__id=product_id, id=cart_item_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('cart')


def delete_to_cart(request, cart_item_id):
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        item = Cart_Item.objects.get(cart=cart, id=cart_item_id)
        item.delete()
    except ObjectDoesNotExist:
        pass

    return redirect('cart')


def CartView(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = {}
    try:
        if request.user.is_authenticated:
            cart_items = Cart_Item.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = cart.cart_items.all()

        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity

    except ObjectDoesNotExist:
        pass

    tax = (5*total)/100
    grand_total = tax + total

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, "cart.html", context)


@login_required(login_url='login')
def checkout(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = {}
    try:

        if request.user.is_authenticated:
            cart_items = Cart_Item.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = cart.cart_items.all()

        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity

    except ObjectDoesNotExist:
        pass

    tax = (5*total)/100
    grand_total = tax + total

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'checkout.html', context)
