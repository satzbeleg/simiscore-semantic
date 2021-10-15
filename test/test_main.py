from starlette.testclient import TestClient
from app.main import app, srvurl


def test_read_main():
    client = TestClient(app)
    response = client.get(f"{srvurl}/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_item_id_none():
    client = TestClient(app)
    response = client.get(f"{srvurl}/items/")
    assert response.status_code == 200
    assert response.json() == {"item_id": None}


def test_valid_item_id():
    client = TestClient(app)
    response = client.get(f"{srvurl}/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": None}


def test_valid_query():
    client = TestClient(app)
    response = client.get(f"{srvurl}/items/42?q=23")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "23"}


def test_validation_error_item():
    client = TestClient(app)
    response = client.get(f"{srvurl}/items/abc")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "item_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_response_fail_invalid_query():
    client = TestClient(app)
    response = client.get(f"{srvurl}/items/42/[ab]")
    assert response.status_code == 404


def test_docs_reachable():
    client = TestClient(app)
    response = client.get(f"{srvurl}/docs")
    assert response.status_code == 200


# FURTHER INFORMATION
# https://fastapi.tiangolo.com/tutorial/testing/
