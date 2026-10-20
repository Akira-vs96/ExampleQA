from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_lecture_contains_all_fifteen_topics() -> None:
    response = client.get("/api/lecture7/topics")
    topics = response.json()
    assert response.status_code == 200
    assert len(topics) == 15
    assert [topic["id"] for topic in topics] == list(range(1, 16))
    assert all(topic["short_answer"] for topic in topics)


def test_single_lecture_topic_and_unknown_topic() -> None:
    response = client.get("/api/lecture7/topics/10")
    assert response.status_code == 200
    assert "breakpoint()" in response.json()["question"]
    assert client.get("/api/lecture7/topics/99").status_code == 404


def test_lab_contains_three_debug_cases() -> None:
    response = client.get("/api/lab7/examples")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {"division", "discount", "maximum"}


def test_example_has_buggy_fixed_code_and_report() -> None:
    response = client.get("/api/lab7/examples/discount")
    data = response.json()
    assert response.status_code == 200
    assert "percent / 100" in data["fixed_code"]
    assert data["report"]["тест нәтижесі"] == "2/2 тест өтті."


def test_debug_run_returns_variables_at_breakpoint() -> None:
    response = client.post(
        "/api/lab7/debug/run",
        json={"example_id": "maximum", "breakpoint_line": 4},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["breakpoint_line"] == 4
    assert data["variables"]["current"] == "4"
    assert data["buggy_result"] == "2"
    assert data["fixed_result"] == "9"


def test_unknown_example_returns_not_found() -> None:
    assert client.get("/api/lab7/examples/unknown").status_code == 404


def test_legacy_example_url_still_works() -> None:
    assert client.get("/api/examples/division").status_code == 200
