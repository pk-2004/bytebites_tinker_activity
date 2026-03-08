"""Unit tests for the ByteBites backend logic."""

import pytest

from bytebites import Item, ItemCollection, Transaction, Customer


def test_item_creation_and_repr():
    item = Item(name="Spicy Burger", price=5.99, category="Entrees", popularity=4.5)
    assert item.name == "Spicy Burger"
    assert item.price == 5.99
    assert item.category == "Entrees"
    assert item.popularity == 4.5
    # repr contains the name and price
    assert "Spicy Burger" in repr(item)
    assert "price=5.99" in repr(item)


def test_item_invalid_values():
    with pytest.raises(ValueError):
        Item(name="Bad", price=-1, category="Misc")
    with pytest.raises(ValueError):
        Item(name="Bad", price=1, category="Misc", popularity=6)


def test_item_collection_operations():
    burger = Item("Burger", 3.5, "Entrees")
    soda = Item("Soda", 1.25, "Drinks")
    dessert = Item("Pie", 2.0, "Desserts")
    coll = ItemCollection([burger, soda, dessert])

    # filtering
    drinks = coll.filter_by_category("Drinks")
    assert drinks == [soda]
    assert coll.filter_by_category("Unknown") == []

    # in‑place sort by price
    coll.sort_by_price()
    assert coll.items == [soda, dessert, burger]
    coll.sort_by_price(reverse=True)
    assert coll.items == [burger, dessert, soda]

    # sorted_by_popularity returns a new list, original order unchanged
    burger.popularity = 2.0
    soda.popularity = 4.0
    dessert.popularity = 3.0
    sorted_pop = coll.sorted_by_popularity()
    assert sorted_pop == [soda, dessert, burger]
    assert coll.items != sorted_pop

    assert "ItemCollection" in repr(coll)


def test_transaction_methods_and_repr():
    a = Item("A", 1, "X")
    b = Item("B", 2, "Y")
    t = Transaction([a])
    t.add_item(b)

    assert t.total_cost() == 3
    assert t.item_count() == 2

    # items_sorted helper
    sorted_items = t.items_sorted(key=lambda i: i.price, reverse=True)
    assert sorted_items == [b, a]

    assert "Transaction" in repr(t)


def test_customer_history_and_validation():
    cust = Customer("Alice")
    assert not cust.is_real_user()

    txn = Transaction()
    txn.add_item(Item("Candy", 0.5, "Desserts"))
    cust.add_transaction(txn)

    assert cust.is_real_user()
    assert cust.purchase_history == [txn]
    assert cust.total_spent() == pytest.approx(0.5)
    assert cust.transaction_count() == 1
    assert "Alice" in repr(cust)


def test_customer_name_required():
    with pytest.raises(ValueError):
        Customer("")