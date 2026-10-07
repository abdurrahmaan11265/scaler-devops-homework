import pytest
from app.catalog import create_app, BOOKS


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    for b in BOOKS:
        b["available"] = b["id"] != 3
    return app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_list_books(client):
    r = client.get("/books")
    assert r.status_code == 200
    assert len(r.get_json()) == 3


def test_get_book(client):
    assert client.get("/books/1").get_json()["title"] == "The Phoenix Project"


def test_missing_book(client):
    assert client.get("/books/99").status_code == 404


def test_borrow_then_conflict(client):
    assert client.post("/books/1/borrow").status_code == 200
    assert client.post("/books/1/borrow").status_code == 409
