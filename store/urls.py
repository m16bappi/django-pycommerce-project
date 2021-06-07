from django.urls import path
from .views import *

urlpatterns = [
    path('', store, name='store'),
    path('<slug:category_slug>/', store, name='product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetails.as_view(), name='product_details')
]
