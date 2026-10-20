"""Duplicate code көрсетуге арналған бастапқы refund модулі."""


def normalize_items(items):
    normalized = []
    for item in items:
        name = item["name"].strip().lower()
        price = float(item["price"])
        quantity = int(item.get("quantity", 1))
        normalized.append({"name": name, "price": price, "quantity": quantity})
    return normalized


def refund_total(items):
    """Қайтарылатын тауарлардың жалпы сомасын есептеу."""
    total = 0
    for item in normalize_items(items):
        total += item["price"] * item["quantity"]
    return total
