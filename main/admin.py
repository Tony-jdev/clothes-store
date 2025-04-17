from django.contrib import admin
from .models import Category, Product

# Registred models for admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'is_visible', 'sort')
    list_display_links = ('name', 'id')
    list_editable = ('is_visible', 'sort')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'price', 'discount', 'is_available', 'sort', 'created_at', 'updated_at')
    list_display_links = ('name', 'id')
    list_editable = ('is_available', 'sort', 'price', 'discount')

    list_filter = ['is_available', 'created_at', 'updated_at']
