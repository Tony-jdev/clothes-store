from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def popular_list(request):
    products = Product.objects.filter(is_available=True)[:3]

    return render(request, 'main/index/index.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)

    return render(request, 'main/product/detail.html', {'product': product})



