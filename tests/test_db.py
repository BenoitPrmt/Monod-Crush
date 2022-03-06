import sqlite3

import pytest
from flask import Flask
from flask.testing import FlaskCliRunner

from flaskr.db import get_db


def test_get_close_db(app: Flask):
    """ Within an application context, get_db should return the same connection each time it’s called.
     After the context, the connection should be closed."""

    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner: FlaskCliRunner, monkeypatch: pytest.MonkeyPatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
