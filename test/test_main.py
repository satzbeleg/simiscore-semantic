import pytest
from starlette.testclient import TestClient

from app.main import app, srvurl


@pytest.fixture
def test_sentences():
    return [
        "Einen Brief quer durch die USA schicken – in nur 10 Tagen!",
        "Eine revolutionäre Entwicklung, dauerte der Postversand um 1850 ein"
        "bis zwei Monate.",
        "Möglich machte es der sogenannte Pony-Express.",
        "Am 3. April 1860 begann eine Stafette furchtloser junger Männer, "
        "entlang der mehr als 3000 km langen Strecke zwischen Kalifornien und "
        "Missouri zuzustellen – hoch zu Ross, den widrigen Wetterverhältnissen"
        " und Überfällen trotzend.",
        "Allem Pioniergeist zum Trotz schienen die Gründer jedoch aufs Pferd "
        "gesetzt zu haben.",
        "Denn bereits 18 Monate später wurde der Pony-Express eingestellt.",
        "Zwei Tage, nachdem das erste transkontinentale Telegramm per "
        "verschickt wurde.",
    ]


def almost_equal(val1, val2, accuracy=10 ** -5):
    return abs(val1 - val2) < accuracy


def test_read_info():
    client = TestClient(app)
    response = client.get(f"{srvurl}/")
    assert response.status_code == 200
    assert response.json().get("version") == "0.1.0"
    assert response.json().get("sbert") == {
        "model": "paraphrase-multilingual-MiniLM-L12-v2",
    }


def test_docs_reachable():
    client = TestClient(app)
    response = client.get(f"{srvurl}/docs")
    assert response.status_code == 200


def test_post_request(test_sentences):
    client = TestClient(app)
    response = client.post(f"{srvurl}/similarities/", json=test_sentences)
    result = [
        response.json()["matrix"][i][i] for i in range(len(test_sentences))
    ]
    assert response.status_code == 200
    assert all(almost_equal(val1, 1) for val1 in result)


def test_post_empty_list():
    client = TestClient(app)
    response = client.post(f"{srvurl}/similarities/", json=[])
    assert response.status_code == 200
    assert response.json() == {"ids": [], "matrix": [[0.0]]}


def test_generate_warning_for_truncation(test_sentences):
    long_sent = " ".join(test_sentences).replace(".", " ")
    test_sentences.insert(0, long_sent)
    client = TestClient(app)
    response = client.post(f"{srvurl}/similarities/", json=test_sentences)
    assert response.status_code == 200
    assert "truncated" in response.json()
    assert len(response.json()["truncated"]) == 1
