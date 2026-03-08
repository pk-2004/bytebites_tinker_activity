classDiagram
    class Item {
        +String name
        +float price
        +String category
        +float popularity
        +__post_init__()
        +__repr__()
    }
    class ItemCollection {
        -List~Item~ items
        +add_item(Item)
        +filter_by_category(String) List~Item~
        +__repr__()
    }
    class Transaction {
        -List~Item~ items
        +add_item(Item)
        +total_cost() float
        +__repr__()
    }
    class Customer {
        -String name
        -List~Transaction~ purchase_history
        +add_transaction(Transaction)
        +is_real_user() bool
        +__repr__()
    }

    ItemCollection "1" o-- "*" Item : contains
    Transaction "1" o-- "*" Item : includes
    Customer "1" o-- "*" Transaction : has