import pytest
from django.urls import reverse
from django.test import Client


# @pytest.mark.django_db
# def test_payment_process_url_get():
#     client = Client()

#     from orders.models import Order
#     order = Order.objects.create(
#         first_name='Test', last_name='User', email='test@example.com',
#         address='Test Address', postal_code='12345', city='Test City'
#     )

#     session = client.session
#     session['order_id'] = order.id
#     session.save()

#     url = reverse('payment:process')
#     response = client.get(url)
#     assert response.status_code in [302, 303]


@pytest.mark.django_db
def test_payment_completed_url():
    client = Client()
    url = reverse('payment:completed')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_payment_canceled_url():
    client = Client()
    url = reverse('payment:canceled')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_payment_webhook_url_post():
    client = Client()
    url = reverse('payment:webhook')

    headers = {
        'HTTP_STRIPE_SIGNATURE': 'test_signature'
    }

    response = client.post(url, data='{}', content_type='application/json', **headers)
    assert response.status_code in [200, 400]
