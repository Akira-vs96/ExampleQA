"""Refund қатесін түзетуге арналған unit және regression тесттері."""

from decimal import Decimal

import pytest

from lab8.order_service import OrderItem, OrderValidationError
from lab8.refund_service import calculate_refund


def test_refund_returns_full_subtotal_when_it_is_below_paid_total() -> None:
    """Unit test: рұқсат етілген қайтарым толық есептеледі."""
    items = [OrderItem("Cable", Decimal("2500"), 2)]

    assert calculate_refund(items, Decimal("6000")) == Decimal("5000.00")


def test_refund_rejects_negative_paid_total() -> None:
    """Unit test: жарамсыз төлем қабылданбайды."""
    with pytest.raises(OrderValidationError, match="теріс"):
        calculate_refund([OrderItem("Cable", Decimal("100"))], Decimal("-1"))


def test_regression_refund_never_exceeds_paid_total() -> None:
    """Regression test: 15 000 ₸ тауар үшін 12 000 ₸-ден артық қайтарылмайды."""
    items = [OrderItem("Mouse", Decimal("7500"), 2)]

    assert calculate_refund(items, Decimal("12000")) == Decimal("12000")
