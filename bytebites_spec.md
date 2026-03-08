# ByteBites Backend Specification

This document captures the initial feature request from the client and
serves as a high-level specification for the core backend data models
and logic needed by the ByteBites application.

## Customer Management

- **Track customers** by name.
- Maintain **purchase history** (list of transactions) for each customer.
- Provide a simple method to verify whether a customer is a "real user"
  (e.g. has at least one transaction and a non-empty name).

## Food Items

Each item sold in the ByteBites store must include:

- `name`: descriptive title (e.g. "Spicy Burger").
- `price`: non-negative float value.
- `category`: general grouping (e.g. "Drinks", "Desserts").
- `popularity`: rating between 0 and 5 (defaults to 0).

## Item Collection

- Maintain a **digital list** (collection) of all available items.
- Support filtering by category so customers can browse specific groups
  (e.g. show only "Drinks").

## Transactions

- When a user selects items, bundle them into a **transaction**.
- Transaction stores the selected items and can compute the **total cost**.

---

These requirements will drive the implementation of the corresponding
Python data classes and unit tests in the repository.
