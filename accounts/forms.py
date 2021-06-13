from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Accounts


class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    class Meta:
        model = Accounts
        fields = ['first_name', 'last_name', 'username',
                  'email', 'phone_number', 'password1', 'password2']
