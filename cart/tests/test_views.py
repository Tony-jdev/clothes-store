import pytest
from django.urls import reverse
from django.test import Client
from main.models import Product, Category

# Створення категорії для тесту
@pytest.fixture
def category():
    return Category.objects.create(name="Test Category", slug="test-category")

# Створення продукту, який використовуватиметься в тестах
@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        category=category,
        price=100,
        discount=10
    )

# Клієнт із доступом до сесії
@pytest.fixture
def client_with_session():
    return Client()


@pytest.mark.django_db
def test_cart_add_valid(client_with_session, product):
    """
    Тестує додавання продукту до кошика:
    - перевіряє статус код та редирект
    - перевіряє, що сесійний кошик зберігає правильну кількість товару
    """
    url = reverse("cart:cart_add", args=[product.id])
    data = {
        "quantity": 2,
        "override": False
    }
    response = client_with_session.post(url, data)

    # Перевірка редиректу після додавання
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")

    # Перевірка вмісту кошика в сесії
    session_cart = client_with_session.session.get("cart")
    assert session_cart is not None
    assert str(product.id) in session_cart
    assert session_cart[str(product.id)]["quantity"] == 2


@pytest.mark.django_db
def test_cart_remove(client_with_session, product):
    """
    Тестує поступове видалення товару з кошика:
    - перше видалення зменшує кількість
    - друге — повністю видаляє товар
    """
    # Додаємо товар
    add_url = reverse("cart:cart_add", args=[product.id])
    client_with_session.post(add_url, {"quantity": 2, "override": False})

    # Перше видалення: має залишитися 1 одиниця
    remove_url = reverse("cart:cart_remove", args=[product.id])
    response = client_with_session.post(remove_url)
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")

    session_cart = client_with_session.session.get("cart")
    assert str(product.id) in session_cart
    assert session_cart[str(product.id)]["quantity"] == 1

    # Друге видалення: товар повністю видаляється
    response = client_with_session.post(remove_url)
    session_cart = client_with_session.session.get("cart")
    assert str(product.id) not in session_cart

@pytest.mark.django_db
def test_cart_detail_view(client_with_session, product):
    """
    Перевіряє, що сторінка перегляду кошика працює правильно:
    - повертає статус 200
    - передає контекст із кошиком
    - використовує правильний шаблон
    """
    # Додаємо товар до кошика
    add_url = reverse("cart:cart_add", args=[product.id])
    client_with_session.post(add_url, {"quantity": 1, "override": False})

    url = reverse("cart:cart_detail")
    response = client_with_session.get(url)

    assert response.status_code == 200
    assert "cart" in response.context
    assert "cart/detail.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_cart_add_ajax(client_with_session, product):
    """
    Перевіряє AJAX-додавання товару до кошика:
    - відповідь повертає JSON із підтвердженням успіху
    - містить назву продукту та кількість товарів у кошику
    """
    url = reverse("cart:cart_add_ajax", args=[product.id])
    response = client_with_session.get(url)

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["product"] == product.name
    assert data["cart_count"] == 1

