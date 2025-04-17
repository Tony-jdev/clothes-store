import pytest
from django.urls import reverse
from django.test import Client
from orders.forms import OrderCreateForm
from orders.models import Order


@pytest.mark.django_db
def test_order_create_form_valid_data():
    """Тестування форми OrderCreateForm з валідними даними"""
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'address': 'Street 1',
        'postal_code': '12345',
        'city': 'Kyiv'
    }
    
    form = OrderCreateForm(data=data)
    assert form.is_valid()  # Перевірка, чи є форма валідною


@pytest.mark.django_db
def test_order_create_form_invalid_data():
    """Тестування форми OrderCreateForm з невалідними даними"""
    data = {
        'first_name': '',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'address': 'Street 1',
        'postal_code': '12345',
        'city': 'Kyiv'
    }
    
    form = OrderCreateForm(data=data)
    assert not form.is_valid()  # Перевірка, чи форма не є валідною через відсутність імені


@pytest.mark.django_db
def test_order_create_form_save():
    """Тестування збереження форми OrderCreateForm"""
    data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane@example.com',
        'address': 'Street 2',
        'postal_code': '54321',
        'city': 'Lviv'
    }
    
    form = OrderCreateForm(data=data)
    assert form.is_valid()  
    
    order = form.save(commit=False)
    assert order.first_name == 'Jane'  
    assert order.last_name == 'Doe'  


@pytest.mark.django_db
def test_order_create_form_with_request():
    """Тестування форми OrderCreateForm з передачею request в kwargs"""
    request = None  # Сюди можна додати фейковий об'єкт request
    data = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice@example.com',
        'address': 'Street 3',
        'postal_code': '67890',
        'city': 'Odessa'
    }

    form = OrderCreateForm(data=data, request=request)
    assert form.is_valid()  
    assert form.request == request  


@pytest.mark.django_db
def test_order_create_form_empty_fields():
    """Тестування форми OrderCreateForm з порожніми полями"""
    data = {
        'first_name': '',
        'last_name': '',
        'email': '',
        'address': '',
        'postal_code': '',
        'city': ''
    }

    form = OrderCreateForm(data=data)
    assert not form.is_valid()  
    assert 'first_name' in form.errors  
    assert 'last_name' in form.errors  
    assert 'email' in form.errors  
    assert 'address' in form.errors  
    assert 'postal_code' in form.errors  
    assert 'city' in form.errors  
