from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from calcstack.api.app import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_root_serves_web_ui(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>calcstack</title>" in response.text


def test_static_asset_is_mounted(client: TestClient) -> None:
    response = client.get("/static/index.html")
    assert response.status_code == 200
    assert "calc-form" in response.text
