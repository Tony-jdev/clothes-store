from django.test import TestCase
from django.contrib.admin.sites import site
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from orders.admin import OrderAdmin, OrderItemInline

class OrderAdminTest(TestCase):
    def setUp(self):
        # Адмін користувач
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.client.login(username='admin', password='adminpass')

    def test_order_model_registered_in_admin(self):
        self.assertIn(Order, site._registry)

    def test_order_admin_list_display(self):
        ma = site._registry[Order]
        self.assertEqual(ma.list_display, ['id', 'first_name', 'last_name', 'email',
                                           'address', 'postal_code', 'city', 'paid',
                                           'created', 'updated'])

    def test_order_admin_list_filter(self):
        ma = site._registry[Order]
        self.assertEqual(ma.list_filter, ['paid', 'created', 'updated'])

    def test_order_admin_has_orderitem_inline(self):
        ma = site._registry[Order]
        self.assertIn(OrderItemInline, ma.inlines)

    def test_admin_order_changelist_accessible(self):
        url = reverse('admin:orders_order_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_order_add_page_accessible(self):
        url = reverse('admin:orders_order_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
