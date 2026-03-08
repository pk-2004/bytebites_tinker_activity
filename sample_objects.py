"""Temporary script to create and inspect ByteBites objects."""

from models import Item, ItemCollection, Transaction, Customer


def main():
    # create some items
    burger = Item(name="Spicy Burger", price=5.99, category="Entrees", popularity=4.5)
    soda = Item(name="Soda", price=1.25, category="Drinks")
    pie = Item(name="Pie", price=2.0, category="Desserts", popularity=3.0)

    print("Items created:")
    print(burger)
    print(soda)
    print(pie)
    print()

    # item collection
    coll = ItemCollection([burger, soda, pie])
    print("Collection repr:", coll)

    # filter by category
    drinks = coll.filter_by_category("Drinks")
    print("Drinks only:", drinks)

    # sorting the menu
    coll.sort_by_price()
    print("Menu sorted by price:", coll)
    print("Menu sorted by popularity (copy):", coll.sorted_by_popularity())
    print()

    # transaction using sorted items for nice receipt
    txn = Transaction()
    # intentionally add out of order
    txn.add_item(pie)
    txn.add_item(burger)
    txn.add_item(soda)
    print("Transaction items sorted by name:", txn.items_sorted(key=lambda i: i.name))
    print("Item count:", txn.item_count())
    print("Total cost:", txn.total_cost())
    print()

    # customer
    cust = Customer("Alice")
    print("New customer:", cust)
    cust.add_transaction(txn)
    print("After purchase:", cust)
    print("Is real user?", cust.is_real_user())
    print("Transactions recorded:", cust.transaction_count())
    print("Total spent:", cust.total_spent())


if __name__ == "__main__":
    main()
