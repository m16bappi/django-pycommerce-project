from django.shortcuts import render

def Cart(request):
    return render(request, "cart.html")
