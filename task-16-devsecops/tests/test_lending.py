import pytest
from app.lending import create_app, LOANS


@pytest.fixture
def client():
    LOANS.clear()
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    assert client.get("/health").get_json()["status"] == "ok"


def test_lend_and_list(client):
    r = client.post("/loans/alice", json={"book": "Accelerate"})
    assert r.status_code == 201
    assert client.get("/loans/alice").get_json()["books"] == ["Accelerate"]


def test_validation(client):
    assert client.post("/loans/alice", json={}).status_code == 400


def test_limit(client):
    for b in ["a", "b", "c"]:
        client.post("/loans/bob", json={"book": b})
    assert client.post("/loans/bob", json={"book": "d"}).status_code == 409


def test_return(client):
    client.post("/loans/carol", json={"book": "x"})
    assert client.delete("/loans/carol").status_code == 204
    assert client.get("/loans/carol").get_json()["books"] == []
