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

    def __repr__(self) -> str:
        return (
            f"Customer(name={self.name!r}, "
            f"purchase_history={self.purchase_history!r})"
        )
