"""Deterministic fixtures shared across laboratories; no tests use an external API."""

import os
from importlib import import_module

import pytest

pytest_plugins = ["scripts.sro_pytest"]


@pytest.fixture
def pricing():
    return import_module(
        "lab6.before.pricing" if os.getenv("QA_VARIANT") == "before" else "qa_shop.pricing"
    )


@pytest.fixture
def shop_app(tmp_path):
    from app.main import create_app

    return create_app(tmp_path / "shop.sqlite3")


@pytest.fixture
def shop_client(shop_app):
    from fastapi.testclient import TestClient

    with TestClient(shop_app) as client:
        yield client


@pytest.fixture
def credentials():
    return {"username": "qa_student", "password": "Test_password_2026"}


@pytest.fixture
def signed_client(shop_client, credentials):
    assert shop_client.post("/api/shop/register", json=credentials).status_code == 201
    assert shop_client.post("/api/shop/login", json=credentials).status_code == 200
    return shop_client
