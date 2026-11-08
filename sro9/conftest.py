from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from scripts.sro_pytest import pytest_configure as pytest_configure
from sro9.app import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(create_app()) as api_client:
        yield api_client
