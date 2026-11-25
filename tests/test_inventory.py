import pytest

from src.inventory import Inventory


def test_add_stock():
    inventory = Inventory()
    inventory.add_stock("pen", 2)
    inventory.add_stock("pen", 3)
    assert inventory.stock["pen"] == 5


def test_remove_stock():
    inventory = Inventory()
    inventory.add_stock("pen", 5)
    inventory.remove_stock("pen", 2)
    assert inventory.stock["pen"] == 3


def test_insufficient_stock():
    inventory = Inventory()
    inventory.add_stock("pen", 1)
    with pytest.raises(ValueError, match="not enough stock"):
        inventory.remove_stock("pen", 2)
    assert inventory.stock["pen"] == 1
