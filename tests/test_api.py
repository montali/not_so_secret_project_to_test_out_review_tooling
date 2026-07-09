from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from calcstack.api.app import app


@pytest.fixture(autouse=True)
def isolated_history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("CALCSTACK_HISTORY", str(tmp_path / "history.json"))
    yield


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calc_ok(client: TestClient) -> None:
    response = client.post("/calc", json={"expression": "2 ^ 10"})
    assert response.status_code == 200
    assert response.json() == {"expression": "2 ^ 10", "result": "1024"}


def test_calc_bad_expression_returns_400(client: TestClient) -> None:
    response = client.post("/calc", json={"expression": "1 /"})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_history_records_and_clears(client: TestClient) -> None:
    client.post("/calc", json={"expression": "3 + 4"})
    client.post("/calc", json={"expression": "5 * 5"})

    listed = client.get("/history").json()
    assert [item["result"] for item in listed] == ["7", "25"]

    assert client.delete("/history").status_code == 200
    assert client.get("/history").json() == []
