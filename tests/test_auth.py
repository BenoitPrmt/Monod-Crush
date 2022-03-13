import pytest
from flask import g, Flask, session
from flask.testing import FlaskClient

from conftest import get_flashed_messages, AuthActions
from flaskr.db import get_db


def test_auth(client: FlaskClient, auth: AuthActions):
    assert client.get("/auth/register.py").status_code == 200
    assert client.get("/auth/login").status_code == 200
    assert client.get("/auth/logout").status_code == 302


def test_register(client: FlaskClient, app: Flask):
    response = client.post("/auth/register.py",
                           data={"username": "username", "dateOfBirth": "2020-04-14", "password": "password"})

    # test that successful registration redirects to the login page
    assert "http://localhost/auth/login" == response.headers["Location"]

    # test that the user was inserted into the database
    with app.app_context():
        assert (get_db().execute("SELECT * FROM user WHERE username = 'user'").fetchone() is not None)


@pytest.mark.parametrize(("username", "message"),
                         (("", "Choisissez un nom d'utilisateur !"),
                          ("abc", "Le nom d'utilisateur doit contenir entre 4 et 25 caractères."),
                          ("a" * 26, "Le nom d'utilisateur doit contenir entre 4 et 25 caractères."),
                          ("user1", "Le nom d'utilisateur ne peut pas contenir de chiffres ni de symboles !"),
                          ("username", "Le nom d'utilisateur user est deja pris.")))
def test_register_validate_input_username(client: FlaskClient, username: str, message: str, auth: AuthActions):
    response = auth.register(username=username)
    assert get_flashed_messages(response) == [message]


@pytest.mark.parametrize(("password", "message"),
                         (("", "Remplissez le champ mot de passe."),
                          ("12345", "Le mot de passe doit contenir entre 6 et 25 caractères."),
                          ("1" * 26, "Le mot de passe doit contenir entre 6 et 25 caractères.")))
def test_register_validate_input_username(client: FlaskClient, password: str, message: str, auth: AuthActions):
    response = auth.register(password=password)
    assert get_flashed_messages(response) == [message]


@pytest.mark.parametrize(("date_of_birth", "message"),
                         (("", "Indiquez votre date de naissance !."),))
def test_register_validate_input_date(client: FlaskClient, date_of_birth: str, message: str, auth: AuthActions):
    response = auth.register(date_of_birth=date_of_birth)
    assert get_flashed_messages(response) == [message]


def test_login(client: FlaskClient):
    response = client.post("/auth/login",
                           data={"username": "user", "password": "user"})

    # test that successful login redirects to the index page
    assert "http://localhost/" == response.headers["Location"]

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session.get("user_id") is not None
        assert g.user["username"] == "user"


@pytest.mark.parametrize(("username", "message"),
                         (("a", "Nom d'utilisateur incorrect"),))
def test_login_validate_input_username(username: str, message: str, auth: AuthActions):
    response = auth.login(username=username)
    assert get_flashed_messages(response) == [message]


@pytest.mark.parametrize(("password", "message"),
                         (("a", "Mot de passe incorrect"),))
def test_login_validate_input_password(password: str, message: str, auth: AuthActions):
    response = auth.login(password=password)
    assert get_flashed_messages(response) == [message]


def test_logout(client: FlaskClient, auth: AuthActions):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
