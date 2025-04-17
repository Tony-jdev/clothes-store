import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_order_create_url():
    """Тестування правильності роботи URL для створення замовлення"""
    url = reverse('orders:order_create')
    response = Client().get(url)
    
    # Перевірка, чи відповідає код статусу 200 (ОК)
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_create_view():
    """Тестування виклику view для створення замовлення"""
    url = reverse('orders:order_create')
    response = Client().get(url)
    
    # Перевірка, чи містить відповідь форму для створення замовлення
    assert 'form' in response.context 
    assert response.status_code == 200  
