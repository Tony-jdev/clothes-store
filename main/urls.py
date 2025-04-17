from django.urls import path
from .views import popular_list, product_detail, product_list

app_name = 'main'

urlpatterns = [
    path('', popular_list, name='popular_list'),
    path('shop/', product_list, name='product-list'),
    path('<slug:slug>/', product_detail, name='product-detail'),
    path('shop/category/<slug:category_slug>', product_list, name='filter-by-category')
]
