import datetime
from django.urls import reverse
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib import messages

from carts.models import Cart_Item
from .models import Order, Payment, OrderProduct
from .forms import orderForm


def payment(request, order_number):
    cart_items = Cart_Item.objects.filter(user=request.user)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=order_number)
    context = {
        'order': order,
        'cart_items': cart_items,
        'total': order.order_total - order.tax,
        'tax': order.tax,
        'grand_total': order.order_total,
        'order_number': order.order_number
    }
    return render(request, 'payment.html', context)


def completePayment(request, order_number):
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=order_number)
    print(order)
    payment = Payment.objects.create(
        user=request.user,
        payment_id=order_number,
        payment_method='PayPal',
        amount_paid=order.order_total,
        status='Verified'
    )
    payment.save()
    order.payment = payment
    order.is_active = True
    order.save()

    # move cart item to the order product table

    # reduce the quantity of the products

    # sent mail to the user

    # clear cart item from cart

    return redirect('dashboard')


def placeOrder(request, total=0, quantity=0):
    cart_items = Cart_Item.objects.filter(user=request.user)
    if cart_items.count() <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for item in cart_items:
        total += (item.product.price * item.quantity)
        quantity += item.quantity

    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yy = int(datetime.date.today().strftime('%Y'))
            dd = int(datetime.date.today().strftime('%d'))
            mm = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yy, mm, dd)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            messages.success(request, 'your order placed successfully')
            return HttpResponseRedirect(reverse('payment', args=[order_number]))
        else:
            messages.error(request, 'please complete your forms')
            return redirect('checkout')
    else:
        return redirect('checkout')
