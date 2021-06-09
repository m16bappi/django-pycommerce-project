from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Products
from category.models import Category


def store(request, category_slug=None):
    products = {}

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.all().filter(
            category=category, is_available=True).order_by('id')
    else:
        products = Products.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paginated_products = paginator.get_page(page)
    return render(request, "store.html", {'products': paginated_products})


class ProductDetails(DetailView):
    template_name = "product-detail.html"

    def get_object(self):
        try:
            return Products.objects.get(category__slug=self.kwargs['category_slug'],
                                        slug=self.kwargs['product_slug'])
        except Exception:
            raise Exception


def search(request):
    return HttpResponse('<h1>search</h1>')