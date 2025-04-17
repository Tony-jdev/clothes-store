import pytest
from cart.forms import CartAddProductForm


@pytest.mark.parametrize("quantity_input", [1, 5, 10])
def test_cart_add_product_form_valid_quantity(quantity_input):
    form_data = {'quantity': quantity_input, 'override': False}
    form = CartAddProductForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data['quantity'] == quantity_input
    assert form.cleaned_data['override'] is False


@pytest.mark.parametrize("quantity_input", [0, 11, 'abc', -3])
def test_cart_add_product_form_invalid_quantity(quantity_input):
    form_data = {'quantity': quantity_input, 'override': False}
    form = CartAddProductForm(data=form_data)
    assert not form.is_valid()
    assert 'quantity' in form.errors


def test_cart_add_product_form_default_override():
    form_data = {'quantity': 1}
    form = CartAddProductForm(data=form_data)
    assert form.is_valid()
    # 'override' має значення за замовчуванням False
    assert form.cleaned_data['override'] is False


def test_cart_add_product_form_override_true():
    form_data = {'quantity': 2, 'override': True}
    form = CartAddProductForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data['override'] is True
