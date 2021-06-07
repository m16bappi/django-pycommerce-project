from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from .models import Products
from category.models import Category


def store(request, category_slug=None):
    context = {}

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        context['products'] = Products.objects.all().filter(category=category, is_available=True)
    else:
        context['products'] = Products.objects.all().filter(is_available=True)
    return render(request, "store.html", context)


class ProductDetails(DetailView):
    template_name = "product-detail.html"

    def get_object(self):
        try:
            return Products.objects.get(category__slug=self.kwargs['category_slug'], slug=self.kwargs['product_slug'])
        except Exception:
            raise Exception
