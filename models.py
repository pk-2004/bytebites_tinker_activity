"""Scaffold for the ByteBites backend models.

Four classes, built bottom-up:
    Item            - info about a food item the user chooses
    ItemCollection  - the menu: every Item, with search/filter/sort helpers
    Transaction     - the selected items for one order, and its cost
    Customer        - a customer's name and purchase history

Every method below is a stub. Fill them in one class at a time,
starting with Item.
"""

from typing import List, Optional


class Item:
    """A single food item on the menu."""

    def __init__(self, name: str, price: float, category: str,
                 popularity: float = 0.0) -> None:
        # TODO: raise ValueError if price is negative
        self.name = name
        self.price = price
        self.category = category
        self.popularity = popularity

    def describe(self) -> str:
        """Return a readable one-liner, e.g. 'Latte (Drinks) - $3.50'."""
        # TODO: build and return the string
        pass


class ItemCollection:
    """The menu: holds every Item and helps you search through them."""

    def __init__(self) -> None:
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """Add one item to the menu."""
        # TODO: append to self.items
        pass

    def remove_item(self, name: str) -> None:
        """Remove the item with this name, if it is on the menu."""
        # TODO: find the matching item and remove it
        pass

    def find_by_name(self, name: str) -> Optional[Item]:
        """Return the item with this name, or None if there isn't one."""
        # TODO: loop through self.items and return the first match
        pass

    def filter_by_category(self, category: str) -> List[Item]:
        """Return a new list of the items in this category."""
        # TODO: build a list of items whose category matches
        pass

    def sort_by_price(self) -> List[Item]:
        """Return a new list of the items, cheapest first."""
        # TODO: use sorted() with a key - do not reorder self.items
        pass

    def sort_by_popularity(self) -> List[Item]:
        """Return a new list of the items, most popular first."""
        # TODO: use sorted() with a key and reverse=True
        pass


class Transaction:
    """One order: the items a customer selected, and what they cost."""

    def __init__(self, transaction_id: str) -> None:
        self.transaction_id = transaction_id
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """Add one item to this order."""
        # TODO: append to self.items
        pass

    def remove_item(self, name: str) -> None:
        """Remove the item with this name from this order."""
        # TODO: find the matching item and remove it
        pass

    def item_count(self) -> int:
        """How many items are in this order."""
        # TODO: return the length of self.items
        pass

    def total_cost(self) -> float:
        """Add up the price of every item in this order."""
        # TODO: add the prices
        pass


class Customer:
    """A customer and the orders they have placed."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.purchase_history: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Record a completed order for this customer."""
        # TODO: append to self.purchase_history
        pass

    def transaction_count(self) -> int:
        """How many orders this customer has placed."""
        # TODO: return the length of self.purchase_history
        pass

    def total_spent(self) -> float:
        """Add up total_cost() across every order."""
        # TODO: sum total_cost() for each transaction
        pass

    def favorite_category(self) -> Optional[str]:
        """The category this customer buys most often, or None if no orders."""
        # TODO: loop over every transaction, then every item inside it,
        #       count each category in a dict, return the most common key
        pass
