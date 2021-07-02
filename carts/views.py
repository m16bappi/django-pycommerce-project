from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
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

    try:
        items = Cart_Item.objects.get(product=product, cart=cart)
        if len(product_variation) > 1:
            for data in product_variation:
                items.variation.add(data)
        items.quantity += 1
        items.variation.add()
        items.save()
    except ObjectDoesNotExist:
        items = Cart_Item.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if len(product_variation) > 1:
            for data in product_variation:
                items.variation.add(data)
        items.save()
    return redirect('cart')


def remove_to_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        item = Cart_Item.objects.get(cart=cart, product__id=product_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('cart')


def delete_to_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        item = Cart_Item.objects.get(cart=cart, product__id=product_id)
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


def checkout(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = {}
    try:
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
