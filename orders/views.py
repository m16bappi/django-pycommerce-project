from django.shortcuts import redirect, render, HttpResponse
from carts.models import Cart_Item
from .models import Order
from .forms import orderForm
import datetime


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
            return redirect('checkout')
    else:
        return redirect('checkout')
