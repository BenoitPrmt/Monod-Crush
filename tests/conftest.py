import html
import os
import re
import tempfile
from typing import Iterator, List

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from werkzeug.test import TestResponse

from flaskr import create_app
from flaskr.db import init_db, populate_db

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
        populate_db()
        # get_db().executescript(_data_sql)

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

    def register(self, *, username: str = "username",
                 date_of_birth: str = "2000-01-01",
                 password: str = "password") -> TestResponse:
        """Register helper function for testing"""

        return self._client.post(
            "/auth/register",
            data={"username": username, "dateOfBirth": date_of_birth, "password": password},
        )

    def login(self, *, username: str = "user", password: str = "user") -> TestResponse:
        """Login helper function for testing"""

        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def admin_login(self) -> TestResponse:
        """Login with admin account """
        return self._client.post(
            "/auth/login", data={"username": "admin", "password": "admin"}
        )

    def logout(self) -> TestResponse:
        """Logout helper function for testing"""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client: FlaskClient) -> AuthActions:
    """Create a AuthActions object for testing"""
    return AuthActions(client)


def get_flashed_messages(response: TestResponse) -> List[str]:
    """Get flashed messages from a html response"""
    regex = re.compile(r'<li class="alert alert-\w*">(.*?)</li>')
    # replace escaped html characters
    data = html.unescape(response.data.decode("utf8"))
    return re.findall(regex, data)
