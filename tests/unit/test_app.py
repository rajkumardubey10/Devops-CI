from src.app import home, health_check, get_item


def test_home():
    response = home()

    assert "FastAPI CI Demo" in response
    assert "Available Endpoints" in response


def test_health_check():
    response = health_check()

    assert response == {"status": "ok"}


def test_get_item_without_query():
    response = get_item(10)

    assert response == {
        "item_id": 10,
        "query": None
    }


def test_get_item_with_query():
    response = get_item(10, "laptop")

    assert response == {
        "item_id": 10,
        "query": "laptop"
    }