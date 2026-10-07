"""Lending service: records which member has which book. Kept deliberately
small so the security tooling around it is the focus."""
import os
from flask import Flask, jsonify, request

LOANS = {}


def create_app():
    app = Flask(__name__)
    app.config["MAX_LOANS"] = int(os.environ.get("MAX_LOANS", "3"))

    @app.get("/health")
    def health():
        return jsonify(status="ok", max_loans=app.config["MAX_LOANS"])

    @app.get("/loans/<member>")
    def member_loans(member):
        return jsonify(member=member, books=LOANS.get(member, []))

    @app.post("/loans/<member>")
    def lend(member):
        body = request.get_json(silent=True) or {}
        book = body.get("book")
        if not isinstance(book, str) or not book.strip():
            return jsonify(error="book is required"), 400
        books = LOANS.setdefault(member, [])
        if len(books) >= app.config["MAX_LOANS"]:
            return jsonify(error="loan limit reached"), 409
        books.append(book.strip())
        return jsonify(member=member, books=books), 201

    @app.delete("/loans/<member>")
    def return_all(member):
        LOANS.pop(member, None)
        return "", 204

    return app


app = create_app()
