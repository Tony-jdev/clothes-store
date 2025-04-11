from django.urls import path
from .views import popular_list, product_detail

app_name = 'main'

urlpatterns = [
    path('', popular_list, name='popular_list'),
    path('<slug:slug>/', product_detail, name='product-detail'),
]