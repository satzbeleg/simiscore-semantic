from starlette.testclient import TestClient

from app.main import app, srvurl
from app.pydantic_models import SentenceInstance


def test_read_main():
    client = TestClient(app)
    response = client.get(f"{srvurl}/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_item_id_none():
    client = TestClient(app)
    response = client.get(f"{srvurl}/similarities/")
    assert response.status_code == 200
    assert response.json() == {"instance_id": None}


def test_valid_item_id():
    client = TestClient(app)
    response = client.get(f"{srvurl}/similarities/abc")
    assert response.status_code == 200
    assert response.json() == {"instance_id": "abc", "q": None}


def test_valid_query():
    client = TestClient(app)
    response = client.get(f"{srvurl}/similarities/42?q=23")
    assert response.status_code == 200
    assert response.json() == {"instance_id": "42", "q": "23"}


def test_response_fail_invalid_query():
    client = TestClient(app)
    response = client.get(f"{srvurl}/similarities/42/[ab]")
    assert response.status_code == 404


def test_docs_reachable():
    client = TestClient(app)
    response = client.get(f"{srvurl}/docs")
    assert response.status_code == 200


# FURTHER INFORMATION
# https://fastapi.tiangolo.com/tutorial/testing/
