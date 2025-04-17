import pytest
from django.urls import reverse, resolve

@pytest.mark.parametrize("url_name, expected_view", [
    ('main:popular_list', 'main.views.popular_list'),
    ('main:product-list', 'main.views.product_list'),
    ('main:product-detail', 'main.views.product_detail'),
    ('main:filter-by-category', 'main.views.product_list'),
])
def test_urls_resolve_to_correct_view(url_name, expected_view):
    url = reverse(url_name)
    view = resolve(url).view_name
    assert view == expected_view
