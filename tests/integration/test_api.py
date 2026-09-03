from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "FastAPI CI Demo" in response.text


def test_get_item_endpoint():
    response = client.get("/items/10?q=laptop")

    assert response.status_code == 200

    assert response.json() == {
        "item_id": 10,
        "query": "laptop"
    }


def test_get_item_without_query():
    response = client.get("/items/10")

    assert response.status_code == 200

    assert response.json() == {
        "item_id": 10,
        "query": None
    }


def test_invalid_item_id():
    response = client.get("/items/abc")

    assert response.status_code == 422