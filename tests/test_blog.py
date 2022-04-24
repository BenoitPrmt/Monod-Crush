from datetime import date

import pytest
from flask import Flask
from flask.testing import FlaskClient

from flaskr.db import get_db
from tests.conftest import AuthActions, get_flashed_messages


def test_index(client: FlaskClient, auth: AuthActions):
    response = client.get("/")
    assert b"Se connecter" in response.data
    assert "Créer un Compte".encode() in response.data

    auth.login()
    response = client.get("/")
    assert "Se déconnecter".encode() in response.data
    assert b"user" in response.data

    assert b"test body" in response.data
    assert b"par un utilisateur anonyme" in response.data
    assert date(year=2018, month=1, day=1).strftime('%a %d %b %Y').encode() in response.data
    assert b'href="/post/1/edit"' in response.data


@pytest.mark.parametrize("path", ("/post/new", "/post/1/edit"))
def test_login_required_get(client: FlaskClient, path: str):
    response = client.get(path)
    assert response.headers["Location"] in ("http://localhost/auth/login", "/auth/login")


@pytest.mark.parametrize("path", ("/post/1/delete", "/post/1/report", "/post/1/like"))
def test_login_required_post(client: FlaskClient, path: str):
    response = client.post(path)
    assert response.headers["Location"] in ("http://localhost/auth/login", "/auth/login")


def test_author_required(app: Flask, client: FlaskClient, auth: AuthActions):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/post/1/edit").status_code == 403
    assert client.post("post/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize("path", ("/post/2/update", "/post/2/delete", "/post/2/report", "/post/2/like"))
def test_exists_required(client: FlaskClient, auth: AuthActions, path: str):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(app: Flask, client: FlaskClient, auth: AuthActions):
    auth.login()
    assert client.get("/post/new").status_code == 200
    response = client.post("/post/new", data={"body": "post2", "anonymous": "on"})
    assert get_flashed_messages(response) == []

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 2


def test_update(app: Flask, client: FlaskClient, auth: AuthActions):
    auth.login()
    assert client.get("/post/1/edit").status_code == 200
    response = client.post("post/1/edit", data={"body": "updated"})
    assert get_flashed_messages(response) == []

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post["body"] == "updated"


@pytest.mark.parametrize("path", ("/new", "post/1/edit"))
def test_create_update_validate(client: FlaskClient, auth: AuthActions, path: str):
    auth.login()

    # anonymous is useless for update
    response = client.post("/post/1/edit", data={"body": "1" * 301, "anonymous": "on"})
    assert get_flashed_messages(response) == [
        ('is-warning', 'Le message ne peut pas dépasser 300 caractères. Soyez plus concis.')]

    response = client.post("/post/1/edit", data={"body": "", "anonymous": "on"})
    assert get_flashed_messages(response) == [
        ('is-warning', 'Le message ne peut pas être vide.')]


def test_delete(client: FlaskClient, auth: AuthActions, app: Flask):
    auth.login()
    response = client.post("post/1/delete")
    assert response.headers["Location"] in ("http://localhost/", "/")

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post is None
