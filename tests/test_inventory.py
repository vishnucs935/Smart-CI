import pytest
from src.inventory import Inventory


def test_add_stock():
    inventory = Inventory()
    inventory.add_stock("Pen", 10)
    assert inventory.get_stock("Pen") == 10


def test_add_stock_accumulates():
    inventory = Inventory()
    inventory.add_stock("Pen", 10)
    inventory.add_stock("Pen", 5)
    assert inventory.get_stock("Pen") == 15


def test_remove_stock():
    inventory = Inventory()
    inventory.add_stock("Pen", 10)
    inventory.remove_stock("Pen", 3)
    assert inventory.get_stock("Pen") == 7


def test_remove_all_stock():
    inventory = Inventory()
    inventory.add_stock("Pen", 10)
    inventory.remove_stock("Pen", 10)
    assert inventory.get_stock("Pen") == 0


def test_removing_too_much_raises_and_preserves_stock():
    inventory = Inventory()
    inventory.add_stock("Pen", 5)

    with pytest.raises(ValueError):
        inventory.remove_stock("Pen", 10)

    assert inventory.get_stock("Pen") == 5


def test_removing_missing_item_raises():
    inventory = Inventory()
    with pytest.raises(ValueError):
        inventory.remove_stock("Book", 1)


def test_different_products_have_separate_stock():
    inventory = Inventory()
    inventory.add_stock("Pen", 10)
    inventory.add_stock("Book", 5)
    assert inventory.get_stock("Pen") == 10
    assert inventory.get_stock("Book") == 5


def test_inventories_have_independent_stock():
    inventory1 = Inventory()
    inventory2 = Inventory()

    inventory1.add_stock("Pen", 10)

    assert inventory1.get_stock("Pen") == 10
    assert inventory2.get_stock("Pen") == 0
