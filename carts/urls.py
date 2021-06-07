from django.urls import path

from .views import *

urlpatterns = [
    path('', Cart, name='cart')
]
