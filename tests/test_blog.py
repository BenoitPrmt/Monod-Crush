import pytest
from flask import Flask
from flask.testing import FlaskClient

from flaskr.db import get_db
from tests.conftest import AuthActions


def test_index(client: FlaskClient, auth: AuthActions):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log In" not in response.data
    assert b"Register" not in response.data
    assert b"Log Out" in response.data
    assert b"user" in response.data

    # assert b"test title" in response.data
    # assert b"by test on 2018-01-01" in response.data
    # assert b"test\nbody" in response.data
    # assert b'href="/1/update"' in response.data

@pytest.mark.skip
@pytest.mark.parametrize("path", ("post/create", "post/1/edit", "post/1/delete"))
def test_login_required(client: FlaskClient, path: str):
    response = client.get(path)
    assert response.history[0].status_code == 302
    assert response.headers["Location"] == "http://localhost/auth/login"


@pytest.mark.skip
def test_author_required(app: Flask, client: FlaskClient, auth: AuthActions):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.skip
@pytest.mark.parametrize("path", ("/2/update", "/2/delete"))
def test_exists_required(client: FlaskClient, auth: AuthActions, path: str):
    auth.login()
    assert client.post(path).status_code == 404


@pytest.mark.skip
def test_create(app: Flask, client: FlaskClient, auth: AuthActions):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 2


@pytest.mark.skip
def test_update(app: Flask, client: FlaskClient, auth: AuthActions):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post["title"] == "updated"


@pytest.mark.skip
@pytest.mark.parametrize("path", ("/create", "/1/update"))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data


@pytest.mark.skip
def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "http://localhost/"

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post is None
