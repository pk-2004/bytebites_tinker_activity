"""Backend models for the ByteBites campus food ordering app.

Four classes, built bottom-up:
    Item            - info about a food item the user chooses
    ItemCollection  - the menu: every Item, with search/filter/sort helpers
    Transaction     - the selected items for one order, and its cost
    Customer        - a customer's name and purchase history
"""

from typing import List, Optional


class Item:
    """A single food item on the menu."""

    def __init__(self, name: str, price: float, category: str,
                 popularity: float = 0.0) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.name = name
        self.price = price
        self.category = category
        self.popularity = popularity

    def describe(self) -> str:
        """Return a readable one-liner, e.g. 'Latte (Drinks) - $3.50'."""
        return f"{self.name} ({self.category}) - ${self.price:.2f}"


class ItemCollection:
    """The menu: holds every Item and helps you search through them."""

    def __init__(self) -> None:
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """Add one item to the menu."""
        self.items.append(item)

    def remove_item(self, name: str) -> None:
        """Remove the item with this name. Does nothing if it isn't found."""
        item = self.find_by_name(name)
        if item is not None:
            self.items.remove(item)

    def find_by_name(self, name: str) -> Optional[Item]:
        """Return the item with this name, or None if there isn't one."""
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

    def filter_by_category(self, category: str) -> List[Item]:
        """Return a new list of the items in this category."""
        matches = []
        for item in self.items:
            if item.category.lower() == category.lower():
                matches.append(item)
        return matches

    def sort_by_price(self) -> List[Item]:
        """Return a new list of the items, cheapest first."""
        return sorted(self.items, key=lambda item: item.price)

    def sort_by_popularity(self) -> List[Item]:
        """Return a new list of the items, most popular first."""
        return sorted(self.items, key=lambda item: item.popularity, reverse=True)


class Transaction:
    """One order: the items a customer selected, and what they cost."""

    def __init__(self, transaction_id: str) -> None:
        self.transaction_id = transaction_id
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """Add one item to this order."""
        self.items.append(item)

    def remove_item(self, name: str) -> None:
        """Remove the item with this name. Does nothing if it isn't found."""
        for item in self.items:
            if item.name.lower() == name.lower():
                self.items.remove(item)
                return

    def item_count(self) -> int:
        """How many items are in this order."""
        return len(self.items)

    def total_cost(self) -> float:
        """Add up the price of every item in this order."""
        total = 0.0
        for item in self.items:
            total += item.price
        return total


class Customer:
    """A customer and the orders they have placed."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.purchase_history: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Record a completed order for this customer."""
        self.purchase_history.append(transaction)

    def transaction_count(self) -> int:
        """How many orders this customer has placed."""
        return len(self.purchase_history)

    def total_spent(self) -> float:
        """Add up total_cost() across every order."""
        total = 0.0
        for transaction in self.purchase_history:
            total += transaction.total_cost()
        return total

    def favorite_category(self) -> Optional[str]:
        """The category this customer buys most often, or None if no orders."""
        counts = {}
        for transaction in self.purchase_history:
            for item in transaction.items:
                counts[item.category] = counts.get(item.category, 0) + 1
        if not counts:
            return None
        return max(counts, key=counts.get)
