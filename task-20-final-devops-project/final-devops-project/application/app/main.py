"""Library API: the one application the whole project is built around.
Books are kept in a JSON file on a persistent volume, settings come from a
ConfigMap, the admin token from a Secret, and /metrics feeds Prometheus."""
import json
import os
import threading
from pathlib import Path

from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUESTS = Counter("library_requests_total", "requests by endpoint and status", ["endpoint", "status"])
LATENCY = Histogram("library_request_seconds", "request latency", ["endpoint"])
_lock = threading.Lock()


def create_app():
    app = Flask(__name__)
    app.config["LIBRARY_NAME"] = os.environ.get("LIBRARY_NAME", "Campus Library")
    app.config["LOAN_DAYS"] = int(os.environ.get("LOAN_DAYS", "14"))
    app.config["ADMIN_TOKEN"] = os.environ.get("ADMIN_TOKEN", "")
    app.config["DATA_FILE"] = Path(os.environ.get("DATA_DIR", "/tmp")) / "books.json"

    def load():
        f = app.config["DATA_FILE"]
        if f.exists():
            return json.loads(f.read_text())
        return [{"id": 1, "title": "The Phoenix Project", "author": "Gene Kim", "available": True},
                {"id": 2, "title": "Accelerate", "author": "Nicole Forsgren", "available": True}]

    def save(books):
        f = app.config["DATA_FILE"]
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(books))

    def track(endpoint, status):
        REQUESTS.labels(endpoint, str(status)).inc()

    @app.get("/health")
    def health():
        track("/health", 200)
        return jsonify(status="ok", library=app.config["LIBRARY_NAME"], loan_days=app.config["LOAN_DAYS"])

    @app.get("/ready")
    def ready():
        ok = app.config["DATA_FILE"].parent.exists()
        track("/ready", 200 if ok else 503)
        return (jsonify(ready=ok), 200 if ok else 503)

    @app.get("/books")
    def list_books():
        with LATENCY.labels("/books").time():
            books = load()
        track("/books", 200)
        return jsonify(books)

    @app.post("/books")
    def add_book():
        if request.headers.get("X-Admin-Token") != app.config["ADMIN_TOKEN"]:
            track("/books", 401)
            return jsonify(error="admin token required"), 401
        body = request.get_json(silent=True) or {}
        if not body.get("title") or not body.get("author"):
            track("/books", 400)
            return jsonify(error="title and author are required"), 400
        with _lock:
            books = load()
            book = {"id": max([b["id"] for b in books] + [0]) + 1, "title": body["title"],
                    "author": body["author"], "available": True}
            books.append(book)
            save(books)
        track("/books", 201)
        return jsonify(book), 201

    @app.post("/books/<int:book_id>/borrow")
    def borrow(book_id):
        with _lock:
            books = load()
            for b in books:
                if b["id"] == book_id:
                    if not b["available"]:
                        track("/borrow", 409)
                        return jsonify(error="already borrowed"), 409
                    b["available"] = False
                    save(books)
                    track("/borrow", 200)
                    return jsonify(b)
        track("/borrow", 404)
        return jsonify(error="book not found"), 404

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app


app = create_app()
