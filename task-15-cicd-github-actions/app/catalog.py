"""A tiny library catalog API. Small on purpose: the point of this task is
the pipeline around it, not the application."""
from flask import Flask, jsonify, request

BOOKS = [
    {"id": 1, "title": "The Phoenix Project", "author": "Gene Kim", "available": True},
    {"id": 2, "title": "Site Reliability Engineering", "author": "Google", "available": True},
    {"id": 3, "title": "Accelerate", "author": "Nicole Forsgren", "available": False},
]


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/books")
    def list_books():
        return jsonify(BOOKS)

    @app.get("/books/<int:book_id>")
    def get_book(book_id):
        for book in BOOKS:
            if book["id"] == book_id:
                return jsonify(book)
        return jsonify(error="book not found"), 404

    @app.post("/books/<int:book_id>/borrow")
    def borrow(book_id):
        for book in BOOKS:
            if book["id"] == book_id:
                if not book["available"]:
                    return jsonify(error="already borrowed"), 409
                book["available"] = False
                return jsonify(book)
        return jsonify(error="book not found"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
