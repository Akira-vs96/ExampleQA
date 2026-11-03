"""The same application at unit, integration, system and acceptance levels."""

from decimal import Decimal

import pytest

from qa_shop.pricing import (
    discounted_total,
    line_total,
    order_total,
    shipping_cost,
    transition_order,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "function,args,expected",
    [
        (line_total, ("2500", 2), Decimal("5000.00")),
        (discounted_total, ("10000", 20), Decimal("8000.00")),
        (shipping_cost, ("10000",), Decimal("0.00")),
        (order_total, ([("2000", 6)], 20), Decimal("10600.00")),
        (transition_order, ("new", "paid"), "paid"),
    ],
)
def test_five_units(function, args, expected):
    assert function(*args) == expected


@pytest.mark.integration
def test_registration_persists_without_exposing_secrets(shop_client, shop_app, credentials):
    response = shop_client.post("/api/shop/register", json=credentials)
    assert response.status_code == 201
    assert set(response.json()) == {"id", "username"}
    with shop_app.state.shop_store.connect() as connection:
        row = connection.execute("SELECT * FROM users").fetchone()
    assert row["username"] == credentials["username"]
    assert credentials["password"] not in row["password_hash"]


@pytest.mark.integration
def test_session_can_be_reloaded_from_storage(signed_client, shop_app):
    from qa_shop.store import Store

    store = Store(shop_app.state.shop_store.path)
    user = store.user_for_token(signed_client.cookies["qa_session"])
    assert user["username"] == "qa_student"


@pytest.mark.system
def test_register_login_search_quote_logout(shop_client, credentials):
    assert shop_client.post("/api/shop/register", json=credentials).status_code == 201
    assert shop_client.post("/api/shop/login", json=credentials).status_code == 200
    product = shop_client.get("/api/shop/products", params={"q": "keyboard"}).json()[0]
    response = shop_client.post(
        "/api/shop/quote",
        json={
            "items": [{"product_id": product["id"], "quantity": 2}],
            "percent": 0,
        },
    )
    assert response.status_code == 200
    assert response.json()["total"] == "10000.00"
    assert shop_client.delete("/api/shop/session").status_code == 204
    assert shop_client.get("/api/shop/me").status_code == 401


@pytest.mark.acceptance
def test_customer_pays_delivery_after_discount(signed_client):
    response = signed_client.post(
        "/api/shop/quote",
        json={
            "items": [{"product_id": 1, "quantity": 2}],
            "percent": 20,
        },
    )
    assert response.json() == {
        "user_id": 1,
        "subtotal": "10000.00",
        "discounted": "8000.00",
        "shipping": "1000.00",
        "total": "9000.00",
        "currency": "KZT",
    }


@pytest.mark.acceptance
def test_unregistered_customer_cannot_quote(shop_client):
    response = shop_client.post(
        "/api/shop/quote",
        json={
            "items": [{"product_id": 1, "quantity": 1}],
        },
    )
    assert response.status_code == 401
