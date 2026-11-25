from src.cart import Cart


def test_total_with_discount():
    cart = Cart()
    cart.add("pen", 50, 2)
    assert cart.total(discount=10) == 106.2


def test_empty_cart():
    assert Cart().total() == 0
