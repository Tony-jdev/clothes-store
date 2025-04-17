# main/tests/test_models.py

import pytest
from django.urls import reverse
from main.models import Category, Product

# FIXTURES
pytestmark = pytest.mark.django_db

@pytest.fixture
def category():
    return Category.objects.create(
        name="Test Category",
        slug="test-category"
    )

@pytest.fixture
def product(category):
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
    assert category.name == "Test Category"
    assert category.slug == "test-category"
    assert category.is_visible is True

def test_category_get_absolute_url(category):
    expected_url = reverse('main:filter-by-category', args=[category.slug])
    assert category.get_absolute_url() == expected_url

# PRODUCT TESTS

def test_product_creation(product):
    assert product.name == "Test Product"
    assert product.price == 100.00
    assert product.discount == 10.0

def test_product_sell_price(product):
    assert product.sell_price() == 90.00  # 10% off

def test_product_category(product, category):
    assert product.category == category

# PARAMETRIZED TESTS (розширення)
@pytest.mark.parametrize("price,discount,expected_price", [
    (100.00, 0.0, 100.00),
    (200.00, 25.0, 150.00),
    (99.99, 10.0, 89.99),
    (50.00, 50.0, 25.00),
])
def test_sell_price_parametrized(category, price, discount, expected_price):
    product = Product.objects.create(
        name=f"Product {price}-{discount}",
        slug=f"product-{price}-{discount}",
        category=category,
        price=price,
        discount=discount,
        description="..."
    )
    assert product.sell_price() == round(expected_price, 2)
