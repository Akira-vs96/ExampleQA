"""Task 4: the same expectation with the corrected endpoint."""

from fastapi.testclient import TestClient


def test_product_url(client: TestClient) -> None:
    response = client.get("/api/products/1")
    assert response.status_code == 200, response.text
    assert response.json()["id"] == 1
