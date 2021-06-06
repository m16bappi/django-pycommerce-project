from django.shortcuts import render
from store.models import Products

def HomeView(request):
    products = Products.objects.all().filter(is_available=True)
    return render(request, 'index.html', {'products': products})
