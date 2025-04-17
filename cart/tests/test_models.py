import pytest
from decimal import Decimal
from django.conf import settings
from django.test import RequestFactory
from main.models import Product, Category
from cart.cart import Cart


@pytest.fixture
def category():
    """Створює тестову категорію продуктів."""
    return Category.objects.create(name="Test Category", slug="test-category")


@pytest.fixture
def product(category):
    """Створює тестовий продукт із знижкою 10%."""
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        category=category,
        price=Decimal("100.00"),
        discount=10.0
    )


@pytest.fixture
def product2(category):
    """Створює другий тестовий продукт із знижкою 20%."""
    return Product.objects.create(
        name="Second Product",
        slug="second-product",
        category=category,
        price=Decimal("50.00"),
        discount=20.0
    )


@pytest.fixture
def request_with_session():
    """Ініціалізує об'єкт запиту з сесією."""
    factory = RequestFactory()
    request = factory.get('/')
    middleware = __import__('django.contrib.sessions.middleware').contrib.sessions.middleware.SessionMiddleware(lambda r: r)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.fixture
def cart(request_with_session):
    """Створює об'єкт кошика, пов’язаний із сесією."""
    return Cart(request_with_session)


@pytest.mark.django_db
def test_add_product_to_cart(cart, product):
    """Перевіряє додавання продукту до кошика з кількістю."""
    cart.add(product=product, quantity=2)
    cart_items = list(cart)
    assert len(cart_items) == 1
    assert cart_items[0]['product'] == product
    assert cart_items[0]['quantity'] == 2
    assert Decimal(cart_items[0]['price']) == Decimal('100.00')


@pytest.mark.django_db
def test_override_quantity(cart, product):
    """Перевіряє перевизначення кількості продукту в кошику."""
    cart.add(product=product, quantity=1)
    cart.add(product=product, quantity=5, override_quantity=True)
    assert len(cart) == 5


@pytest.mark.django_db
def test_remove_product(cart, product):
    """Перевіряє видалення продукту з кошика."""
    cart.add(product=product, quantity=3)
    cart.remove(product)
    assert len(cart) == 2
    cart.remove(product)
    cart.remove(product)
    assert len(cart) == 0


@pytest.mark.django_db
def test_clear_cart(cart, product, product2):
    """Перевіряє очищення кошика."""
    cart.add(product=product, quantity=1)
    cart.add(product=product2, quantity=1)
    assert len(cart) == 2
    cart.clear()
    assert len(cart.session.get(settings.CART_SESSION_ID, {})) == 0


@pytest.mark.django_db
def test_get_total_price(cart, product, product2):
    """Перевіряє розрахунок загальної вартості з урахуванням знижок."""
    cart.add(product=product, quantity=2)
    cart.add(product=product2, quantity=1)

    _ = list(cart)  # Щоб додати 'product' до кожного item
    total = Decimal(cart.get_total_price())
    expected = round((100 - 10) * 2 + (50 - 10), 2)
    assert total == expected
