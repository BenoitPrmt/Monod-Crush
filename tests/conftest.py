import os
import tempfile
from typing import Iterator

from werkzeug.test import TestResponse

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app() -> Iterator[Flask]:
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    """ helper class for testing authentication """

    def __init__(self, client: FlaskClient) -> None:
        self._client = client

    def login(self, username: str = "test", password: str = "test") -> TestResponse:
        """Login helper function for testing"""
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self) -> TestResponse:
        """Logout helper function for testing"""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client: FlaskClient) -> AuthActions:
    """Create a AuthActions object for testing"""
    return AuthActions(client)
