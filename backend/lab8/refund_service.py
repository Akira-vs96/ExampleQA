"""Қайтарым сомасын ортақ тапсырыс есептеу функциясымен есептеу."""

from collections.abc import Iterable
from decimal import Decimal

from lab8.order_service import OrderItem, OrderValidationError, calculate_subtotal


def calculate_refund(items: Iterable[OrderItem], paid_total: Decimal) -> Decimal:
    """Қайтарым сомасын төленген сомадан асырмай қайтарады."""
    if paid_total < 0:
        raise OrderValidationError("Төленген сома теріс болмауы керек.")
    return min(calculate_subtotal(items), paid_total)
