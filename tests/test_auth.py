import pytest
from flask import g, Flask, session
from flask.testing import FlaskClient

from conftest import get_flashed_messages, AuthActions
from flaskr.db import get_db
from datetime import date, timedelta


def test_auth(client: FlaskClient, auth: AuthActions):
    assert client.get("/auth/register").status_code == 200
    assert client.get("/auth/login").status_code == 200


def test_register(client: FlaskClient, app: Flask):
    response = client.post("/auth/register",
                           data={"username": "username", "dateOfBirth": "2020-04-14", "password": "pa12OU!!45sds"})

    # test that successful registration redirects to the login page
    assert "http://localhost/" == response.headers["Location"]

    # test that the user was inserted into the database
    with app.app_context():
        assert (get_db().execute("SELECT * FROM user WHERE username = 'user'").fetchone() is not None)


@pytest.mark.parametrize(("username", "message"),
                         (("", "Votre nom d'utilisateur doit contenir au moins 3 caractères"),
                          ("a" * 21, "Votre nom d'utilisateur doit contenir 20 caractères maximum"),
                          ("1abc",
                           "Votre nom d'utilisateur doit commencer par une lettre et peut contenir uniquement des lettres,"
                           " nombres, tirets du bas et tirets"),
                          ("-abc",
                           "Votre nom d'utilisateur doit commencer par une lettre et peut contenir uniquement des lettres,"
                           " nombres, tirets du bas et tirets"),
                          ("abc!",
                           "Votre nom d'utilisateur doit commencer par une lettre et peut contenir uniquement des lettres,"
                           " nombres, tirets du bas et tirets"),
                          ("user", "Ce nom d'utilisateur est déjà pris")))
def test_register_validate_input_username(client: FlaskClient, username: str, message: str, auth: AuthActions):
    response = auth.register(username=username)
    assert get_flashed_messages(response) == [("is-warning", message)]


@pytest.mark.parametrize(("password", "message"),
                         (("", "Le mot de passe doit contenir au moins 6 caractères"),
                          ("1" * 26, "Le mot de passe doit contenir 25 caractères maximum")))
def test_register_validate_input_password(client: FlaskClient, password: str, message: str, auth: AuthActions):
    response = auth.register(password=password)
    assert get_flashed_messages(response) == [("is-warning", message)]


@pytest.mark.parametrize(("date_of_birth", "message"),
                         (("", "Le format de la date de naissance est invalide"),
                          ((date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
                           "Vous voyagez dans le temps ? Votre date de naissance doit être dans le passé"),
                          ("1900-04-14", "Veuillez indiquer une date de naissance valide")))
def test_register_validate_input_date(client: FlaskClient, date_of_birth: str, message: str, auth: AuthActions):
    response = auth.register(date_of_birth=date_of_birth)
    assert get_flashed_messages(response) == [("is-warning", message)]


def test_login(client: FlaskClient):
    response = client.post("/auth/login", data={"username": "user", "password": "user"})
    assert get_flashed_messages(response) == []

    # test that successful login redirects to the index page
    assert response.headers["Location"] == "http://localhost/"

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session.get("user_id") is not None
        assert g.user["username"] == "user"


def test_fail_login(auth: AuthActions):
    response = auth.login(username='wrong')
    assert get_flashed_messages(response) == [('is-danger', "Nom d'utilisateur ou mot de passe incorrect")]

    response = auth.login(password='wrong')
    assert get_flashed_messages(response) == [('is-danger', "Nom d'utilisateur ou mot de passe incorrect")]

    response = auth.login(username='wrong', password='wrong')
    assert get_flashed_messages(response) == [('is-danger', "Nom d'utilisateur ou mot de passe incorrect")]

    response = auth.login(username='', password='')
    assert get_flashed_messages(response) == [('is-danger', "Nom d'utilisateur ou mot de passe incorrect")]


def test_logout(client: FlaskClient, auth: AuthActions):
    auth.login()

    with client:
        response = client.get("/auth/logout")
        assert "user_id" not in session
        assert response.headers["Location"] == "http://localhost/"
