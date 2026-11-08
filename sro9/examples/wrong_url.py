"""Task 4: intentionally failing example; run explicitly, outside the normal suite."""

from fastapi.testclient import TestClient


def test_product_url(client: TestClient) -> None:
    response = client.get("/api/producst/1")  # Typo: producst instead of products.
    assert response.status_code == 200, response.text
