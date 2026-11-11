import pytest
from src.pricing import apply_discount, add_tax


def test_discount_basic():
    assert apply_discount(100, 10) == 90


def test_discount_boundaries():
    assert apply_discount(100, 0) == 100
    assert apply_discount(100, 100) == 0


@pytest.mark.parametrize("discount", [-1, -0.01, 100.01, 101])
def test_discount_invalid(discount):
    with pytest.raises(ValueError):
        apply_discount(100, discount)


def test_discount_rounds_to_two_places():
    assert apply_discount(10, 33.333) == 6.67


def test_discount_zero_price():
    assert apply_discount(0, 10) == 0


def test_tax_default():
    assert add_tax(100) == 118


def test_tax_custom_rate():
    assert add_tax(100, 10) == 110


def test_tax_zero_rate():
    assert add_tax(100, 0) == 100


def test_tax_rounds_to_two_places():
    assert add_tax(10, 5.555) == 10.56
