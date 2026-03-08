"""Backend models for the ByteBites application.

This module defines basic classes to manage customers, food items,
collections of items, and transactions. It provides the foundational
logic needed by the app to track users and their purchases.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Item:
    """Represents a food item available for purchase."""

    name: str
    price: float
    category: str
    popularity: float = 0.0

    def __post_init__(self):
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
    """A container for multiple items with filtering support."""

    def __init__(self, items: List[Item] | None = None) -> None:
        self.items: List[Item] = list(items) if items is not None else []

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def filter_by_category(self, category: str) -> List[Item]:
        """Return a list of items whose category matches the argument."""
        return [item for item in self.items if item.category == category]

    def __repr__(self) -> str:
        return f"ItemCollection({self.items!r})"


class Transaction:
    """Represents a customer's purchase made up of multiple items."""

    def __init__(self, items: List[Item] | None = None) -> None:
        self.items: List[Item] = list(items) if items is not None else []

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def total_cost(self) -> float:
        """Compute the total price of all items in the transaction."""
        return sum(item.price for item in self.items)

    def __repr__(self) -> str:
        return f"Transaction(items={self.items!r})"


class Customer:
    """Tracks a customer's identity and their purchase history."""

    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Customer must have a name")
        self.name: str = name
        self.purchase_history: List[Transaction] = []

    def add_transaction(self, txn: Transaction) -> None:
        self.purchase_history.append(txn)

    def is_real_user(self) -> bool:
        """A simple check to determine if this customer appears valid.

        For our purposes we just ensure that they have a nonempty name
        and at least one recorded transaction.  In a real system this
        could involve verifying an email, ID, etc.
        """
        return bool(self.name and self.purchase_history)

    def __repr__(self) -> str:
        return (
            f"Customer(name={self.name!r}, "
            f"purchase_history={self.purchase_history!r})"
        )
