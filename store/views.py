from django.db.models import Q
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

    products_count = products.count()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paginated_products = paginator.get_page(page)

    context = {
        'products': paginated_products,
        'products_count': products_count
    }

    return render(request, "store.html", context)


class ProductDetails(DetailView):
    template_name = "product-detail.html"

    def get_object(self):
        try:
            return Products.objects.get(category__slug=self.kwargs['category_slug'],
                                        slug=self.kwargs['product_slug'])
        except Exception:
            raise Exception


def search(request):
    if request.GET['keyword']:
        keyword = request.GET['keyword']
        products = Products.objects.filter(
            Q(description__icontains=keyword) |
            Q(product_name__icontains=keyword)).order_by('-created_date')

        products_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paginated_products = paginator.get_page(page)

        context = {
            'res': True,
            'products': paginated_products,
            'products_count': products_count
        }

        return render(request, 'search-result.html', context)
    else:
        return render(request, 'search-result.html', {'res': False})
