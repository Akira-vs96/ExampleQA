"""Equivalence classes, ten boundary cases, a decision table and state edges."""

from decimal import Decimal

import pytest

from qa_shop.pricing import TRANSITIONS


@pytest.mark.blackbox
@pytest.mark.parametrize(
    "quantity,valid", [(-1, False), (1, True), (101, False), (1.5, False), (True, False)]
)
def test_five_equivalence_classes(pricing, quantity, valid):
    if valid:
        assert pricing.line_total("100", quantity) == Decimal(100 * quantity)
    else:
        with pytest.raises(ValueError):
            pricing.line_total("100", quantity)


@pytest.mark.blackbox
@pytest.mark.parametrize(
    "operation,args,expected",
    [
        ("line_total", (100, 1), "100.00"),
        ("line_total", (100, 2), "200.00"),
        ("line_total", (100, 99), "9900.00"),
        ("line_total", (100, 100), "10000.00"),
        ("discounted_total", (100, 0), "100.00"),
        ("discounted_total", (100, 1), "99.00"),
        ("discounted_total", (100, 99), "1.00"),
        ("discounted_total", (100, 100), "0.00"),
        ("shipping_cost", ("9999.99",), "1000.00"),
        ("shipping_cost", ("10000.00",), "0.00"),
    ],
)
def test_ten_boundaries(pricing, operation, args, expected):
    assert getattr(pricing, operation)(*args) == Decimal(expected)


@pytest.mark.blackbox
@pytest.mark.parametrize(
    "subtotal,percent,shipping",
    [
        (9000, 0, 1000),
        (9000, 20, 1000),
        (12000, 0, 0),
        (12000, 20, 1000),
    ],
)
def test_delivery_decision_table(pricing, subtotal, percent, shipping):
    assert pricing.shipping_cost(pricing.discounted_total(subtotal, percent)) == shipping


@pytest.mark.whitebox
@pytest.mark.parametrize(
    "state,target",
    [
        ("new", "paid"),
        ("new", "cancelled"),
        ("paid", "shipped"),
        ("paid", "refunded"),
        ("shipped", "completed"),
    ],
)
def test_all_valid_edges(pricing, state, target):
    assert pricing.transition_order(state, target) == target


@pytest.mark.whitebox
@pytest.mark.parametrize(
    "state,target",
    [
        ("shipped", "cancelled"),
        ("completed", "paid"),
        ("cancelled", "new"),
        ("refunded", "shipped"),
        ("unknown", "paid"),
        ("new", "unknown"),
    ],
)
def test_invalid_edges(pricing, state, target):
    with pytest.raises(ValueError):
        pricing.transition_order(state, target)


@pytest.mark.whitebox
def test_every_state_pair(pricing):
    for state in TRANSITIONS:
        for target in TRANSITIONS:
            if target in TRANSITIONS[state]:
                assert pricing.transition_order(state, target) == target
            else:
                with pytest.raises(ValueError):
                    pricing.transition_order(state, target)
