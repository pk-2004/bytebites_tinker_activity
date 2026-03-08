"""Scaffold for ByteBites backend models.

The four primary classes are declared here with their expected
initializers and method stubs.  This file serves as a starting point
for implementing the full functionality described in the specification.
"""

from __future__ import annotations
from typing import List


from dataclasses import dataclass, field


@dataclass
class Item:
    """Represents a food item available for purchase."""

    name: str
    price: float
    category: str
    popularity: float = 0.0

    def __post_init__(self) -> None:
        # validation according to spec
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not (0.0 <= self.popularity <= 5.0):
            raise ValueError("Popularity must be between 0 and 5")

    def __repr__(self) -> str:
        return (
            f"Item(name={self.name!r}, price={self.price:.2f}, "
            f"category={self.category!r}, popularity={self.popularity:.1f})"
        )


class ItemCollection:
    """Container for multiple Item instances with filtering support."""

    def __init__(self, items: List[Item] | None = None) -> None:
        # keep a mutable list internally; copy if provided
        self.items: List[Item] = list(items) if items is not None else []

    def add_item(self, item: Item) -> None:
        """Add an item to the collection."""
        self.items.append(item)

    def filter_by_category(self, category: str) -> List[Item]:
        """Return items matching the given category."""
        return [item for item in self.items if item.category == category]

    # additional helpers
    def sort_by_price(self, reverse: bool = False) -> None:
        """Sort the internal list of items by price in-place."""
        self.items.sort(key=lambda i: i.price, reverse=reverse)

    def sorted_by_popularity(self) -> List[Item]:
        """Return a new list of items ordered by popularity (highest first)."""
        return sorted(self.items, key=lambda i: i.popularity, reverse=True)

    def __repr__(self) -> str:
        return f"ItemCollection({self.items!r})"


class Transaction:
    """Represents a user's purchase made up of several items."""

    def __init__(self, items: List[Item] | None = None) -> None:
        self.items: List[Item] = list(items) if items is not None else []

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def total_cost(self) -> float:
        """Compute and return the total price of all items."""
        return sum(item.price for item in self.items)

    def item_count(self) -> int:
        """How many items are in this transaction."""
        return len(self.items)

    # optional view-friendly method
    def items_sorted(self, *, key=None, reverse: bool = False) -> List[Item]:
        """Return a sorted copy of the transaction items using a key function."""
        return sorted(self.items, key=key, reverse=reverse)

    def __repr__(self) -> str:
        return f"Transaction(items={self.items!r})"


class Customer:
    """Tracks a customer's identity and purchase history."""

    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Customer must have a name")
        self.name: str = name
        self.purchase_history: List[Transaction] = []

    def add_transaction(self, txn: Transaction) -> None:
        self.purchase_history.append(txn)

    def is_real_user(self) -> bool:
        """Simple check for a valid customer (name + history)."""
        return bool(self.name and self.purchase_history)

    # additional convenience
    def total_spent(self) -> float:
        """Sum of costs for every transaction in the history."""
        return sum(txn.total_cost() for txn in self.purchase_history)

    def transaction_count(self) -> int:
        """Number of recorded transactions."""
        return len(self.purchase_history)

    def __repr__(self) -> str:
        return (
            f"Customer(name={self.name!r}, "
            f"purchase_history={self.purchase_history!r})"
        )
