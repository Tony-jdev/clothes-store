from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def popular_list(request):
    products = Product.objects.filter(is_available=True)

    return render(request, 'main/index/index.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)

    return render(request, 'main/product/detail.html', {'product': product})



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'main/product/list.html', {'category' : category, 'categories' : categories, 'products' : products})

