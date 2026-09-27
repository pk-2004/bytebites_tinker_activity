"""A walkthrough of the ByteBites models, one feature at a time.

Run with:  python sample_objects.py
"""

from models import Item, ItemCollection, Transaction, Customer


def show(title: str) -> None:
    """Print a section header so the output is easy to read."""
    print("\n" + title)
    print("-" * len(title))


# 1. Create a few items and look at them ------------------------------------
show("1. Sample items")

latte = Item("Latte", 3.50, "Drinks", popularity=4.8)
cold_brew = Item("Cold Brew", 4.25, "Drinks", popularity=4.1)
bagel = Item("Everything Bagel", 2.75, "Breakfast", popularity=3.9)
burrito = Item("Breakfast Burrito", 6.50, "Breakfast", popularity=4.6)
brownie = Item("Brownie", 2.25, "Desserts", popularity=4.9)
cookie = Item("Cookie", 1.75, "Desserts", popularity=3.2)

for item in [latte, cold_brew, bagel, burrito, brownie, cookie]:
    print(item.describe())

print(f"\nInspecting one item -> name={latte.name}, price={latte.price}, "
      f"category={latte.category}, popularity={latte.popularity}")


# 2. Build the menu ---------------------------------------------------------
show("2. Adding items to the menu")

menu = ItemCollection()
for item in [latte, cold_brew, bagel, burrito, brownie, cookie]:
    menu.add_item(item)

print(f"The menu has {len(menu.items)} items.")


# 3. Sorting ----------------------------------------------------------------
show("3. Menu sorted by price (cheapest first)")
for item in menu.sort_by_price():
    print(f"  ${item.price:5.2f}  {item.name}")

show("3b. Menu sorted by popularity (most popular first)")
for item in menu.sort_by_popularity():
    print(f"  {item.popularity:.1f} stars  {item.name}")

print("\nThe menu's own order is unchanged:",
      [item.name for item in menu.items])


# 4. Filtering and searching ------------------------------------------------
show("4. Filtering by category")

drinks = menu.filter_by_category("Drinks")
print("Drinks:", [item.name for item in drinks])

desserts = menu.filter_by_category("desserts")   # matching ignores case
print("Desserts:", [item.name for item in desserts])

print("Sushi:", menu.filter_by_category("Sushi"), "(no matches)")

found = menu.find_by_name("Brownie")
print("\nfind_by_name('Brownie') ->", found.describe())
print("find_by_name('Pizza')   ->", menu.find_by_name("Pizza"))

menu.remove_item("Cookie")
print(f"\nAfter removing the Cookie, the menu has {len(menu.items)} items.")


# 5. One order and its total ------------------------------------------------
show("5. Building an order")

order1 = Transaction("T-1001")
order1.add_item(latte)
order1.add_item(burrito)
order1.add_item(brownie)

for item in order1.items:
    print(f"  {item.describe()}")
print(f"Order {order1.transaction_id}: {order1.item_count()} items, "
      f"total ${order1.total_cost():.2f}")

order1.remove_item("Brownie")
print(f"After removing the Brownie: {order1.item_count()} items, "
      f"total ${order1.total_cost():.2f}")


# 6. A customer with a purchase history -------------------------------------
show("6. Customer purchase history")

order2 = Transaction("T-1002")
order2.add_item(cold_brew)
order2.add_item(bagel)
order2.add_item(bagel)

maya = Customer("Maya")
maya.add_transaction(order1)
maya.add_transaction(order2)

for transaction in maya.purchase_history:
    print(f"  {transaction.transaction_id}: {transaction.item_count()} items, "
          f"${transaction.total_cost():.2f}")

print(f"\n{maya.name} placed {maya.transaction_count()} orders "
      f"and spent ${maya.total_spent():.2f} in total.")
print(f"Favorite category: {maya.favorite_category()}")

new_customer = Customer("Sam")
print(f"\n{new_customer.name} has no orders yet -> "
      f"total spent ${new_customer.total_spent():.2f}, "
      f"favorite category {new_customer.favorite_category()}")
