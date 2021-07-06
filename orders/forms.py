from django import forms
from django.forms import fields
from .models import Order


class orderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone',
                  'email', 'address_line1', 'address_line2', 'country', 'state',
                  'city', 'order_note']
