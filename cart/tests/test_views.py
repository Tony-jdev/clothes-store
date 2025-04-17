import pytest
from django.urls import reverse
from django.test import Client
from main.models import Product, Category
from decimal import Decimal

@pytest.fixture
def category():
    return Category.objects.create(name="Test Category", slug="test-category")

@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        category=category,
        price=100,
        discount=10
    )

@pytest.fixture
def client_with_session():
    return Client()

@pytest.mark.django_db
def test_cart_add_valid(client_with_session, product):
    url = reverse("cart:cart_add", args=[product.id])
    data = {
        "quantity": 2,
        "override": False
    }
    response = client_with_session.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")

    session_cart = client_with_session.session.get("cart")
    assert session_cart is not None
    assert str(product.id) in session_cart
    assert session_cart[str(product.id)]["quantity"] == 2

@pytest.mark.django_db
def test_cart_remove(client_with_session, product):
    # Додати спочатку продукт із quantity=2
    add_url = reverse("cart:cart_add", args=[product.id])
    client_with_session.post(add_url, {"quantity": 2, "override": False})

    # Перший виклик remove() зменшує quantity до 1
    remove_url = reverse("cart:cart_remove", args=[product.id])
    response = client_with_session.post(remove_url)
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")

    session_cart = client_with_session.session.get("cart")
    # Товар ще є, але кількість зменшилась до 1
    assert str(product.id) in session_cart
    assert session_cart[str(product.id)]["quantity"] == 1

    # Другий виклик remove() повністю видаляє товар
    response = client_with_session.post(remove_url)
    session_cart = client_with_session.session.get("cart")
    assert str(product.id) not in session_cart
@pytest.mark.django_db
def test_cart_detail_view(client_with_session, product):
    url = reverse("cart:cart_detail")
    # додати щось у кошик
    add_url = reverse("cart:cart_add", args=[product.id])
    client_with_session.post(add_url, {"quantity": 1, "override": False})

    response = client_with_session.get(url)
    assert response.status_code == 200
    assert "cart" in response.context
    assert "cart/detail.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_cart_add_ajax(client_with_session, product):
    url = reverse("cart:cart_add_ajax", args=[product.id])
    response = client_with_session.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["product"] == product.name
    assert data["cart_count"] == 1
