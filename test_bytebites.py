"""Tests for ByteBites filtering and order totals.

Run with:  python -m pytest test_bytebites.py -v
"""

import pytest

from models import Item, ItemCollection, Transaction, Customer


@pytest.fixture
def menu():
    """A small menu: two Drinks, two Breakfast items, one Dessert."""
    collection = ItemCollection()
    collection.add_item(Item("Latte", 3.50, "Drinks", 4.8))
    collection.add_item(Item("Cold Brew", 4.25, "Drinks", 4.1))
    collection.add_item(Item("Everything Bagel", 2.75, "Breakfast", 3.9))
    collection.add_item(Item("Breakfast Burrito", 6.50, "Breakfast", 4.6))
    collection.add_item(Item("Brownie", 2.25, "Desserts", 4.9))
    return collection


# --- Filtering by category -------------------------------------------------

def test_filter_returns_every_item_in_the_category(menu):
    names = [item.name for item in menu.filter_by_category("Drinks")]
    assert names == ["Latte", "Cold Brew"]


def test_filter_returns_a_single_item_category(menu):
    desserts = menu.filter_by_category("Desserts")
    assert len(desserts) == 1
    assert desserts[0].name == "Brownie"


def test_filter_ignores_case(menu):
    assert len(menu.filter_by_category("drinks")) == 2
    assert len(menu.filter_by_category("DRINKS")) == 2
    assert len(menu.filter_by_category("DrInKs")) == 2


def test_filter_with_no_matches_returns_empty_list(menu):
    assert menu.filter_by_category("Sushi") == []


def test_filter_on_an_empty_menu_returns_empty_list():
    assert ItemCollection().filter_by_category("Drinks") == []


def test_filter_does_not_change_the_menu(menu):
    menu.filter_by_category("Drinks")
    assert len(menu.items) == 5


def test_filter_returns_a_new_list_not_the_menus_own(menu):
    drinks = menu.filter_by_category("Drinks")
    drinks.clear()
    assert len(menu.items) == 5


def test_filter_returns_the_same_item_objects(menu):
    latte = menu.find_by_name("Latte")
    assert menu.filter_by_category("Drinks")[0] is latte


def test_filter_reflects_a_removed_item(menu):
    menu.remove_item("Cold Brew")
    names = [item.name for item in menu.filter_by_category("Drinks")]
    assert names == ["Latte"]


# --- Calculating an order total --------------------------------------------

def test_total_cost_adds_up_every_item():
    order = Transaction("T-1")
    order.add_item(Item("Latte", 3.50, "Drinks"))
    order.add_item(Item("Breakfast Burrito", 6.50, "Breakfast"))
    order.add_item(Item("Brownie", 2.25, "Desserts"))
    assert order.total_cost() == pytest.approx(12.25)
    assert order.item_count() == 3


def test_total_cost_of_one_item():
    order = Transaction("T-2")
    order.add_item(Item("Cookie", 1.75, "Desserts"))
    assert order.total_cost() == pytest.approx(1.75)


def test_total_cost_counts_a_repeated_item_twice():
    bagel = Item("Everything Bagel", 2.75, "Breakfast")
    order = Transaction("T-3")
    order.add_item(bagel)
    order.add_item(bagel)
    assert order.item_count() == 2
    assert order.total_cost() == pytest.approx(5.50)


def test_total_cost_handles_a_free_item():
    order = Transaction("T-4")
    order.add_item(Item("Latte", 3.50, "Drinks"))
    order.add_item(Item("Free Sample", 0.0, "Desserts"))
    assert order.total_cost() == pytest.approx(3.50)
    assert order.item_count() == 2


def test_total_cost_survives_floating_point_cents():
    order = Transaction("T-5")
    for _ in range(3):
        order.add_item(Item("Chips", 0.10, "Snacks"))
    assert order.total_cost() == pytest.approx(0.30)


def test_total_cost_drops_when_an_item_is_removed():
    order = Transaction("T-6")
    order.add_item(Item("Latte", 3.50, "Drinks"))
    order.add_item(Item("Brownie", 2.25, "Desserts"))
    order.remove_item("Brownie")
    assert order.item_count() == 1
    assert order.total_cost() == pytest.approx(3.50)


def test_removing_a_repeated_item_only_removes_one():
    bagel = Item("Everything Bagel", 2.75, "Breakfast")
    order = Transaction("T-7")
    order.add_item(bagel)
    order.add_item(bagel)
    order.remove_item("Everything Bagel")
    assert order.item_count() == 1
    assert order.total_cost() == pytest.approx(2.75)


def test_customer_total_spent_adds_up_every_order():
    first = Transaction("T-8")
    first.add_item(Item("Latte", 3.50, "Drinks"))
    second = Transaction("T-9")
    second.add_item(Item("Brownie", 2.25, "Desserts"))

    maya = Customer("Maya")
    maya.add_transaction(first)
    maya.add_transaction(second)

    assert maya.transaction_count() == 2
    assert maya.total_spent() == pytest.approx(5.75)


# --- Empty totals ----------------------------------------------------------

def test_empty_order_costs_nothing():
    order = Transaction("T-10")
    assert order.item_count() == 0
    assert order.total_cost() == 0.0


def test_order_emptied_by_removal_costs_nothing():
    order = Transaction("T-11")
    order.add_item(Item("Cookie", 1.75, "Desserts"))
    order.remove_item("Cookie")
    assert order.item_count() == 0
    assert order.total_cost() == 0.0


def test_new_customer_has_spent_nothing():
    sam = Customer("Sam")
    assert sam.transaction_count() == 0
    assert sam.total_spent() == 0.0
    assert sam.favorite_category() is None


def test_customer_with_only_empty_orders_has_spent_nothing():
    sam = Customer("Sam")
    sam.add_transaction(Transaction("T-12"))
    sam.add_transaction(Transaction("T-13"))
    assert sam.transaction_count() == 2
    assert sam.total_spent() == 0.0
    assert sam.favorite_category() is None
