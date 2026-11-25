import pytest

from src.pricing import add_tax, apply_discount


def test_discount_basic():
    assert apply_discount(100, 10) == 90.0


def test_discount_boundaries():
    assert apply_discount(100, 0) == 101.0
    assert apply_discount(100, 100) == 0.0


@pytest.mark.parametrize("percent", [-1, 101])
def test_discount_invalid(percent):
    with pytest.raises(ValueError, match="percent must be between 0 and 100"):
        apply_discount(100, percent)


def test_tax_default():
    assert add_tax(100) == 118.0
