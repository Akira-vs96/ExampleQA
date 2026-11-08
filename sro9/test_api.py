"""Six required cases, HTTP method checks and two stateful integration scenarios."""

import pytest
from fastapi.testclient import TestClient
from httpx import Response

BASE = "/api/products"
PRODUCT = {"name": "Mouse", "price": 2500, "stock": 5}


def assert_product(response: Response, status: int = 200) -> dict:
    assert response.status_code == status, response.text
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert set(data) == {"id", "name", "price", "stock"}
    assert type(data["id"]) is int and data["id"] >= 1
    assert type(data["name"]) is str and 1 <= len(data["name"]) <= 100
    assert type(data["price"]) is int and 0 <= data["price"] <= 1_000_000
    assert type(data["stock"]) is int and 0 <= data["stock"] <= 1000
    return data


def test_tc01_valid_get(client: TestClient) -> None:
    assert assert_product(client.get(f"{BASE}/1")) == {
        "id": 1, "name": "Keyboard", "price": 5000, "stock": 10
    }


def test_tc02_missing_product(client: TestClient) -> None:
    response = client.get(f"{BASE}/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Тауар табылмады."}


def test_tc03_negative_price(client: TestClient) -> None:
    response = client.post(BASE, json=PRODUCT | {"price": -1})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "price"]
    assert response.json()["detail"][0]["type"] == "greater_than_equal"


def test_tc04_string_price(client: TestClient) -> None:
    response = client.post(BASE, json=PRODUCT | {"price": "2500"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_type"


def test_tc05_minimum_price(client: TestClient) -> None:
    data = assert_product(client.post(BASE, json=PRODUCT | {"price": 0}), 201)
    assert data["price"] == 0


def test_tc06_maximum_price(client: TestClient) -> None:
    data = assert_product(client.post(BASE, json=PRODUCT | {"price": 1_000_000}), 201)
    assert data["price"] == 1_000_000


def test_post_creates_resource_and_location(client: TestClient) -> None:
    response = client.post(BASE, json=PRODUCT)
    data = assert_product(response, 201)
    assert response.headers["location"] == f"{BASE}/{data['id']}"
    assert assert_product(client.get(response.headers["location"])) == data


def test_put_requires_complete_replacement(client: TestClient) -> None:
    response = client.put(f"{BASE}/1", json={"price": 3000})
    assert response.status_code == 422
    assert {error["loc"][-1] for error in response.json()["detail"]} == {"name", "stock"}
    assert assert_product(client.get(f"{BASE}/1"))["price"] == 5000


@pytest.mark.parametrize("payload", [{}, {"stock": None}, {"price": True}, {"id": 2}])
def test_patch_rejects_invalid_payload(client: TestClient, payload: dict) -> None:
    assert client.patch(f"{BASE}/1", json=payload).status_code == 422
    assert assert_product(client.get(f"{BASE}/1"))["price"] == 5000


@pytest.mark.parametrize("price", [-1, 1_000_001])
def test_price_outside_limits_does_not_create(client: TestClient, price: int) -> None:
    assert client.post(BASE, json=PRODUCT | {"price": price}).status_code == 422
    response = client.get(BASE)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.integration
def test_it01_create_read_replace_delete(client: TestClient) -> None:
    """POST → GET → PUT → GET → DELETE → GET 404."""
    response = client.post(BASE, json=PRODUCT)
    created = assert_product(response, 201)
    url = response.headers["location"]
    assert assert_product(client.get(url)) == created
    replacement = {"name": "Monitor", "price": 45000, "stock": 3}
    expected = {"id": created["id"], **replacement}
    assert assert_product(client.put(url, json=replacement)) == expected
    assert assert_product(client.get(url)) == expected
    deleted = client.delete(url)
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(url).status_code == 404


@pytest.mark.integration
def test_it02_patch_validation_and_state(client: TestClient) -> None:
    """POST → PATCH → GET → rejected PATCH → GET unchanged → DELETE."""
    response = client.post(BASE, json=PRODUCT)
    created = assert_product(response, 201)
    url = response.headers["location"]
    expected = created | {"stock": 0}
    assert assert_product(client.patch(url, json={"stock": 0})) == expected
    assert assert_product(client.get(url)) == expected
    assert client.patch(url, json={"stock": -1}).status_code == 422
    assert assert_product(client.get(url)) == expected
    assert client.delete(url).status_code == 204


def test_unknown_url_is_404(client: TestClient) -> None:
    assert client.get("/api/producst/1").status_code == 404


def test_delete_is_idempotent_for_resource_state(client: TestClient) -> None:
    assert client.delete(f"{BASE}/1").status_code == 204
    assert client.delete(f"{BASE}/1").status_code == 404
    assert client.get(f"{BASE}/1").status_code == 404
