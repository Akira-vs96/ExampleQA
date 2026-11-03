"""Local security tests: authentication, access control, injection, sessions and headers."""

import sqlite3
import time

import pytest

from qa_shop.store import Store

pytestmark = pytest.mark.security


def test_protected_resource(shop_client):
    assert shop_client.get("/api/shop/me").status_code == 401


def test_forged_session(shop_client):
    shop_client.cookies.set("qa_session", "made-up-token")
    assert shop_client.get("/api/shop/me").status_code == 401


def test_wrong_password(signed_client, credentials):
    response = signed_client.post("/api/shop/login", json={**credentials, "password": "wrongpass"})
    assert response.status_code == 401


def test_sql_injection_fails(shop_client, credentials):
    shop_client.post("/api/shop/register", json=credentials)
    assert (
        shop_client.post(
            "/api/shop/login",
            json={
                "username": "admin' OR '1'='1",
                "password": "anything123",
            },
        ).status_code
        == 422
    )
    assert shop_client.app.state.shop_store.login("' OR 1=1 --", "anything123") is None


def test_xss_is_data(shop_client):
    response = shop_client.get("/api/shop/products", params={"q": "<script>alert(1)</script>"})
    assert response.status_code == 200
    assert response.json() == []
    assert response.headers["content-type"].startswith("application/json")


def test_cookie_flags(signed_client, credentials):
    response = signed_client.post("/api/shop/login", json=credentials)
    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=strict" in cookie
    assert "path=/api/shop" in cookie


def test_https_sets_secure_cookie(shop_client, credentials):
    shop_client.post("/api/shop/register", json=credentials)
    response = shop_client.post("https://testserver/api/shop/login", json=credentials)
    assert "secure" in response.headers["set-cookie"].lower()


def test_logout_revokes_captured_token(signed_client):
    token = signed_client.cookies["qa_session"]
    signed_client.delete("/api/shop/session")
    signed_client.cookies.set("qa_session", token)
    assert signed_client.get("/api/shop/me").status_code == 401


def test_expired_session(signed_client, shop_app):
    with shop_app.state.shop_store.connect() as connection:
        connection.execute("UPDATE sessions SET expires = ?", (time.time() - 1,))
    assert signed_client.get("/api/shop/me").status_code == 401


def test_isolated_sessions(shop_client, credentials):
    store = shop_client.app.state.shop_store
    store.register(**credentials)
    first = store.login(**credentials)
    second = store.login(**credentials)
    assert first != second
    store.logout(first)
    assert store.user_for_token(first) is None
    assert store.user_for_token(second)["username"] == credentials["username"]


def test_duplicate_registration_is_conflict(signed_client, credentials):
    assert signed_client.post("/api/shop/register", json=credentials).status_code == 409


def test_unknown_username_same_public_error(shop_client, credentials):
    assert shop_client.post("/api/shop/login", json=credentials).status_code == 401


def test_password_salts(shop_client):
    store = shop_client.app.state.shop_store
    store.register("first_user", "same_password")
    store.register("second_user", "same_password")
    with store.connect() as connection:
        rows = connection.execute("SELECT salt, password_hash FROM users").fetchall()
    assert rows[0]["salt"] != rows[1]["salt"]
    assert rows[0]["password_hash"] != rows[1]["password_hash"]
    assert len(Store.token_hash("demo")) == 64


@pytest.mark.parametrize("path", ["/api/health", "/api/shop/products", "/shop.html"])
def test_security_headers(shop_client, path):
    response = shop_client.get(path)
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert response.headers["referrer-policy"] == "no-referrer"


@pytest.mark.parametrize(
    "items",
    [
        [],
        [{"product_id": 1, "quantity": -1}],
        [{"product_id": 1, "quantity": True}],
        [{"product_id": 1, "quantity": 1}, {"product_id": 1, "quantity": 1}],
    ],
)
def test_invalid_quote(signed_client, items):
    assert signed_client.post("/api/shop/quote", json={"items": items}).status_code == 422


def test_unknown_product_quote(signed_client):
    assert (
        signed_client.post(
            "/api/shop/quote",
            json={
                "items": [{"product_id": 999, "quantity": 1}],
            },
        ).status_code
        == 404
    )


def test_no_sensitive_response(signed_client):
    response = signed_client.get("/api/shop/me")
    assert set(response.json()) == {"id", "username"}
    assert response.headers["cache-control"] == "no-store"


def test_connection_is_closed_after_transaction(shop_app):
    with shop_app.state.shop_store.connect() as connection:
        assert connection.execute("SELECT 1").fetchone()[0] == 1
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        connection.execute("SELECT 1")


def test_logout_without_session_is_idempotent(shop_client):
    assert shop_client.delete("/api/shop/session").status_code == 204
    assert shop_client.delete("/api/shop/session").status_code == 204


def test_long_query_rejected(shop_client):
    assert shop_client.get("/api/shop/products", params={"q": "a" * 81}).status_code == 422
