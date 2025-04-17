import pytest
from django.urls import reverse
from main.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile

# ----- Фікстури -----

@pytest.fixture
def category():
    """
    Створює тестову категорію для використання в продуктах.
    """
    return Category.objects.create(name="Test Category", slug="test-category")


@pytest.fixture
def image_file():
    """
    Повертає примітивне зображення у вигляді об'єкта SimpleUploadedFile.
    """
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\x47\x49\x46\x38\x89\x61',  # мінімальний вміст GIF-файлу
        content_type='image/jpeg'
    )


@pytest.fixture
def product(category, image_file):
    """
    Створює тестовий продукт, прив’язаний до тестової категорії та зображення.
    """
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        category=category,
        price=100.00,
        discount=10.0,
        is_available=True,
        image=image_file
    )

# ----- Тести представлень (views) -----

@pytest.mark.django_db
def test_popular_list_view(client, category, image_file):
    """
    Перевіряє, що представлення популярних продуктів повертає 200 OK
    і містить потрібний продукт у відповіді.
    """
    Product.objects.create(
        name="Popular Product",
        slug="popular-product",
        category=category,
        price=100.00,
        discount=10.0,
        is_available=True,
        image=image_file
    )

    response = client.get(reverse('main:popular_list'))
    assert response.status_code == 200
    assert b"Popular Product" in response.content


@pytest.mark.django_db
@pytest.mark.parametrize("slug, expected_product_name", [
    ('test-product', "Test Product"),
])
def test_product_detail_view(client, product, slug, expected_product_name):
    """
    Перевіряє, що сторінка деталей продукту повертає 200 OK
    і містить назву відповідного продукту.
    """
    response = client.get(reverse('main:product-detail', args=[slug]))
    assert response.status_code == 200
    assert expected_product_name.encode() in response.content


@pytest.mark.django_db
@pytest.mark.parametrize("category_slug, expected_product_name", [
    ('test-category', "Test Product"),
])
def test_product_list_view_with_category(client, product, category, category_slug, expected_product_name):
    """
    Перевіряє, що список продуктів по категорії повертає 200 OK
    і містить відповідний продукт.
    """
    response = client.get(reverse('main:filter-by-category', args=[category_slug]))
    assert response.status_code == 200
    assert expected_product_name.encode() in response.content


@pytest.mark.django_db
def test_product_list_view_without_category(client, product):
    """
    Перевіряє, що загальний список продуктів повертає 200 OK
    та передає список продуктів у контекст шаблону.
    """
    response = client.get(reverse('main:product-list'))
    assert response.status_code == 200
    assert 'products' in response.context
