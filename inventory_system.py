"""Inventory management system for adding, removing, and tracking items.

This module provides helper functions to manage an in-memory
inventory stored in the module-level `stock_data` dictionary and
persistence helpers to load/save the inventory to a JSON file.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, List, Optional

# Global variable holding item -> quantity mapping
stock_data: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0, logs: Optional[List[str]] = None) -> None:
    """Add quantity of an item to the inventory.

    Parameters:
        item: Name of the item to add. Must be a non-empty string.
        qty: Integer quantity to add (can be positive, negative, or zero to adjust).
        logs: Optional list to append a timestamped operation message to.

    Returns:
        None

    Raises:
        TypeError: If `item` is not a string or `qty` is not an int.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an int")

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item: str, qty: int) -> None:
    """Remove quantity of an item from the inventory.

    If the resulting quantity is less than or equal to zero, the item is removed
    from `stock_data`.

    Parameters:
        item: Name of the item to remove.
        qty: Integer quantity to remove.

    Returns:
        None

    Raises:
        TypeError: If `item` is not a string or `qty` is not an int.
    """
    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an int")

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Item not present: silently ignore
        pass


def get_qty(item: str) -> int:
    """Return the current quantity for `item`.

    Parameters:
        item: Name of the item.

    Returns:
        The quantity as an int. Returns 0 if the item is not present.
    """
    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory data from a JSON file into the module-level `stock_data`.

    If the file does not exist or is invalid JSON, this function leaves
    the current in-memory `stock_data` unchanged and raises the underlying
    exception so callers can decide how to handle it.

    Parameters:
        file: Path to the JSON file.

    Returns:
        None

    Raises:
        ValueError: If data is not a mapping of string→int or cannot be parsed.
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("inventory JSON must contain an object mapping items to quantities")

    stock_data.clear()
    for key, val in data.items():
        if not isinstance(key, str) or not key:
            raise ValueError("inventory keys must be non-empty strings")
        if not isinstance(val, int):
            try:
                val = int(val)
            except Exception as exc:
                raise ValueError("inventory quantities must be integers") from exc
        stock_data[key] = val


def save_data(file: str = "inventory.json") -> None:
    """Save the current `stock_data` to a JSON file.

    Parameters:
        file: Path to write the inventory JSON to.

    Returns:
        None
    """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=2)


def print_data() -> None:
    """Print a simple items report to stdout."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items with quantity below `threshold`.

    Parameters:
        threshold: Numeric threshold under which items are considered low.

    Returns:
        List of item names with quantity < threshold.
    """
    if not isinstance(threshold, int):
        raise TypeError("threshold must be an int")
    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Example usage of the inventory system (runs when executed as a script)."""
    logs: List[str] = []
    add_item("apple", 10, logs)
    add_item("banana", 2, logs)

    remove_item("apple", 3)
    remove_item("orange", 1)  # no-op; orange not present

    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    print_data()


if __name__ == "__main__":
    main()
