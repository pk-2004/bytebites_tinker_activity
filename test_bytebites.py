"""Unit tests for the ByteBites backend logic."""

import pytest

from bytebites import Item, ItemCollection, Transaction, Customer


def test_item_creation_and_repr():
    item = Item(name="Spicy Burger", price=5.99, category="Entrees", popularity=4.5)
    assert item.name == "Spicy Burger"
    assert item.price == 5.99
    assert item.category == "Entrees"
    assert item.popularity == 4.5
    assert "Spicy Burger" in repr(item)


def test_item_invalid_values():
    with pytest.raises(ValueError):
        Item(name="Bad", price=-1, category="Misc")
    with pytest.raises(ValueError):
        Item(name="Bad", price=1, category="Misc", popularity=6)


def test_item_collection_filtering():
    burger = Item("Burger", 3.5, "Entrees")
    soda = Item("Soda", 1.25, "Drinks")
    dessert = Item("Pie", 2.0, "Desserts")
    coll = ItemCollection([burger, soda, dessert])
    drinks = coll.filter_by_category("Drinks")
    assert drinks == [soda]
    assert coll.filter_by_category("Unknown") == []


def test_transaction_total_and_repr():
    a = Item("A", 1, "X")
    b = Item("B", 2, "Y")
    t = Transaction([a])
    t.add_item(b)
    assert t.total_cost() == 3
    assert "Transaction" in repr(t)


def test_customer_history_and_validation():
    cust = Customer("Alice")
    assert not cust.is_real_user()
    txn = Transaction()
    txn.add_item(Item("Candy", 0.5, "Desserts"))
    cust.add_transaction(txn)
    assert cust.is_real_user()
    assert cust.purchase_history == [txn]
    assert "Alice" in repr(cust)


def test_customer_name_required():
    with pytest.raises(ValueError):
        Customer("")
