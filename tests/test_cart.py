import pytest
from src.cart import Cart


def test_total_with_discount():
    cart = Cart()
    cart.add_item("Pen", 50, 2)
    assert cart.total(10) == 106.2


def test_empty_cart():
    cart = Cart()
    assert cart.total() == 0


def test_default_quantity():
    cart = Cart()
    cart.add_item("Pen", 50)
    assert cart.total() == 59


def test_multiple_items_and_quantities():
    cart = Cart()
    cart.add_item("Pen", 10, 2)
    cart.add_item("Book", 100, 1)
    assert cart.total() == 141.6


def test_full_discount():
    cart = Cart()
    cart.add_item("Pen", 100)
    assert cart.total(100) == 0


def test_invalid_discount_reaches_pricing_validation():
    cart = Cart()
    cart.add_item("Pen", 100)
    with pytest.raises(ValueError):
        cart.total(110)


def test_carts_have_independent_items():
    cart1 = Cart()
    cart2 = Cart()
    cart1.add_item("Pen", 50)
    assert cart1.total() == 59
    assert cart2.total() == 0


def test_total_does_not_change_items():
    cart = Cart()
    cart.add_item("Pen", 50)
    cart.total()
    assert len(cart.items) == 1
