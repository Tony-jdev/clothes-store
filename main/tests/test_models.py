import pytest
from django.urls import reverse
from main.models import Category, Product

# Автоматично додає `@pytest.mark.django_db` до всіх тестів у файлі
pytestmark = pytest.mark.django_db

# FIXTURES

@pytest.fixture
def category():
    """
    Створює тестову категорію для використання у тестах.
    """
    return Category.objects.create(
        name="Test Category",
        slug="test-category"
    )

@pytest.fixture
def product(category):
    """
    Створює тестовий продукт, пов'язаний із тестовою категорією.
    """
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        category=category,
        price=100.00,
        discount=10.0,
        description="A test product"
    )

# CATEGORY TESTS

def test_category_creation(category):
    """
    Перевіряє створення категорії з правильними значеннями.
    """
    assert category.name == "Test Category"
    assert category.slug == "test-category"
    assert category.is_visible is True

def test_category_get_absolute_url(category):
    """
    Перевіряє правильність методу get_absolute_url для Category.
    """
    expected_url = reverse('main:filter-by-category', args=[category.slug])
    assert category.get_absolute_url() == expected_url

# PRODUCT TESTS

def test_product_creation(product):
    """
    Перевіряє створення продукту з правильними значеннями.
    """
    assert product.name == "Test Product"
    assert product.price == 100.00
    assert product.discount == 10.0

def test_product_sell_price(product):
    """
    Перевіряє, що метод sell_price() правильно розраховує ціну зі знижкою.
    """
    assert product.sell_price() == 90.00  # 10% off

def test_product_category(product, category):
    """
    Перевіряє зв'язок між продуктом і категорією.
    """
    assert product.category == category

# PARAMETRIZED TESTS

@pytest.mark.parametrize("price,discount,expected_price", [
    (100.00, 0.0, 100.00),
    (200.00, 25.0, 150.00),
    (99.99, 10.0, 89.99),
    (50.00, 50.0, 25.00),
])
def test_sell_price_parametrized(category, price, discount, expected_price):
    """
    Перевіряє метод sell_price() для різних комбінацій цін і знижок.
    """
    product = Product.objects.create(
        name=f"Product {price}-{discount}",
        slug=f"product-{price}-{discount}",
        category=category,
        price=price,
        discount=discount,
        description="..."
    )
    assert product.sell_price() == round(expected_price, 2)
