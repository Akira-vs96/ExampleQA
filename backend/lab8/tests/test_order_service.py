"""Түзетілген тапсырыс және қайтарым логикасының тесттері."""

from decimal import Decimal

import pytest

from lab8.order_service import (
    CustomerType,
    OrderItem,
    OrderValidationError,
    calculate_order,
)
from lab8.refund_service import calculate_refund


def test_regular_customer_total() -> None:
    items = [OrderItem("Keyboard", Decimal("12000"), 2)]

    result = calculate_order(items)

    assert result.subtotal == Decimal("24000.00")
    assert result.total == Decimal("24000.00")


def test_larger_promo_discount_wins() -> None:
    items = [OrderItem("Mouse", Decimal("10000"))]

    result = calculate_order(items, CustomerType.NEW, Decimal(15))

    assert result.discount_percent == Decimal(15)
    assert result.discount_amount == Decimal("1500.00")
    assert result.total == Decimal("8500.00")


def test_vip_discount_wins_over_smaller_promo() -> None:
    items = [OrderItem("Monitor", Decimal("100000"))]

    result = calculate_order(items, CustomerType.VIP, Decimal(10))

    assert result.discount_percent == Decimal(20)
    assert result.total == Decimal("80000.00")


@pytest.mark.parametrize(
    "item",
    [
        OrderItem("", Decimal(10)),
        OrderItem("Cable", Decimal(-1)),
        OrderItem("Cable", Decimal(10), 0),
    ],
)
def test_invalid_item_is_rejected(item: OrderItem) -> None:
    with pytest.raises(OrderValidationError):
        calculate_order([item])


def test_empty_order_is_rejected() -> None:
    with pytest.raises(OrderValidationError, match="кемінде бір"):
        calculate_order([])


@pytest.mark.parametrize("percent", [Decimal(-1), Decimal(101)])
def test_invalid_discount_is_rejected(percent: Decimal) -> None:
    with pytest.raises(OrderValidationError, match="0 мен 100"):
        calculate_order([OrderItem("Cable", Decimal(10))], promo_percent=percent)


def test_refund_reuses_validated_subtotal_and_respects_paid_total() -> None:
    items = [OrderItem("Mouse", Decimal(7500), 2)]

    assert calculate_refund(items, Decimal(12000)) == Decimal(12000)


def test_negative_paid_total_is_rejected() -> None:
    with pytest.raises(OrderValidationError, match="теріс"):
        calculate_refund([OrderItem("Mouse", Decimal(100))], Decimal(-1))
