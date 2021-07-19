from django.urls import path
from .views import *


urlpatterns = [
    path('', placeOrder, name='place-order'),
    path('<int:order_number>/', payment, name='payment'),
    path('payment/<int:order_number>/', completePayment, name='complete-payment')
]
