"""Five functions, parametrization, fixtures, exceptions and rounding edge cases."""

from decimal import Decimal

import pytest

from qa_shop.pricing import amount

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "price,quantity,expected",
    [
        (2500, 2, "5000.00"),
        (0, 1, "0.00"),
        ("1.005", 2, "2.02"),
        (10, 100, "1000.00"),
    ],
)
def test_line_total(pricing, price, quantity, expected):
    assert pricing.line_total(price, quantity) == Decimal(expected)


@pytest.mark.parametrize("quantity", [0, -1, 101, 1.5, True, "2"])
def test_invalid_quantity(pricing, quantity):
    with pytest.raises(ValueError):
        pricing.line_total(100, quantity)


@pytest.mark.parametrize(
    "value", [-1, "NaN", "Infinity", "-Infinity", "abc", True, "1000000001", None, "1e999999"]
)
def test_invalid_amount(value):
    with pytest.raises(ValueError):
        amount(value)


@pytest.mark.parametrize("percent,expected", [(0, "100.00"), (20, "80.00"), (100, "0.00")])
def test_percent(pricing, percent, expected):
    assert pricing.discounted_total(100, percent) == Decimal(expected)


@pytest.mark.parametrize("percent", [-1, 101, 1.5, True, "20"])
def test_invalid_percent(pricing, percent):
    with pytest.raises(ValueError):
        pricing.discounted_total(100, percent)


def test_round_half_up(pricing):
    assert pricing.discounted_total("1.01", 50) == Decimal("0.51")


@pytest.mark.parametrize(
    "total,expected", [("9999.99", "1000.00"), ("10000", "0.00"), ("10000.01", "0.00")]
)
def test_shipping(pricing, total, expected):
    assert pricing.shipping_cost(total) == Decimal(expected)


def test_order_uses_discounted_delivery_threshold(pricing):
    assert pricing.order_total([(2000, 6)], 20) == Decimal("10600.00")


def test_empty_cart(pricing):
    with pytest.raises(ValueError):
        pricing.order_total([])


def test_transition(pricing):
    assert pricing.transition_order("new", "paid") == "paid"
    with pytest.raises(ValueError):
        pricing.transition_order("shipped", "cancelled")
