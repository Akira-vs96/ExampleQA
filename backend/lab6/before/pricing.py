"""Five original defects. This module is never imported by the running application."""

from decimal import Decimal


def line_total(price, quantity):
    return Decimal(str(price)) + quantity  # BUG: addition instead of multiplication.


def discounted_total(subtotal, percent):
    return Decimal(str(subtotal)) * (1 - percent)  # BUG: missing / 100.


def shipping_cost(total):
    return Decimal(0) if Decimal(str(total)) > 10000 else Decimal(1000)  # BUG: boundary.


def order_total(lines, percent=0):
    subtotal = sum(line_total(price, count) for price, count in lines)
    return discounted_total(subtotal, percent) + shipping_cost(subtotal)  # BUG: wrong base.


def transition_order(state, target):
    return target  # BUG: every transition accepted, including cancellation after shipping.
