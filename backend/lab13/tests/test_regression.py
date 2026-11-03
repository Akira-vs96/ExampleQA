"""Ten automated checks for the five reproduced defects and critical HTTP contracts."""

from decimal import Decimal

import pytest

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_multiplication(pricing):
    assert pricing.line_total(2000, 3) == Decimal("6000.00")


def test_percent_conversion(pricing):
    assert pricing.discounted_total(10000, 20) == Decimal("8000.00")


def test_inclusive_free_delivery(pricing):
    assert pricing.shipping_cost(10000) == Decimal("0.00")


def test_delivery_after_discount(pricing):
    assert pricing.order_total([(2000, 6)], 20) == Decimal("10600.00")


def test_prevent_cancellation_after_shipment(pricing):
    with pytest.raises(ValueError):
        pricing.transition_order("shipped", "cancelled")


@pytest.mark.smoke
def test_health_smoke(shop_client):
    assert shop_client.get("/api/health").status_code == 200


@pytest.mark.smoke
def test_catalogue_smoke(shop_client):
    assert len(shop_client.get("/api/shop/products").json()) == 3


def test_case_insensitive_search(shop_client):
    assert shop_client.get("/api/shop/products?q=KEYBOARD").json()[0]["id"] == 1


def test_unknown_product(shop_client):
    assert shop_client.get("/api/shop/products/999").status_code == 404


def test_empty_quote_is_rejected(signed_client):
    assert signed_client.post("/api/shop/quote", json={"items": []}).status_code == 422
