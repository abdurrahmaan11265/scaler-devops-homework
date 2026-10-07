import pytest
from app.main import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("ADMIN_TOKEN", "test-token")
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.get_json()["status"] == "ok"


def test_ready(client):
    assert client.get("/ready").status_code == 200


def test_list_books(client):
    assert len(client.get("/books").get_json()) == 2


def test_add_book_requires_token(client):
    assert client.post("/books", json={"title": "x", "author": "y"}).status_code == 401


def test_add_book(client):
    r = client.post("/books", json={"title": "SRE", "author": "Google"}, headers={"X-Admin-Token": "test-token"})
    assert r.status_code == 201
    assert len(client.get("/books").get_json()) == 3


def test_borrow_twice(client):
    assert client.post("/books/1/borrow").status_code == 200
    assert client.post("/books/1/borrow").status_code == 409


def test_metrics(client):
    client.get("/books")
    assert b"library_requests_total" in client.get("/metrics").data
