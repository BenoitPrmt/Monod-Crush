import sqlite3

import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db() -> sqlite3.Connection:
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None) -> None:
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db() -> None:
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def populate_db() -> None:
    """Push fake data to the database."""
    from faker import Faker

    db = get_db()

    fake = Faker('fr_FR')

    db.execute("INSERT INTO user (username, password, admin) VALUES (?, ?, ?)",
               ("admin", generate_password_hash("admin"), 1))

    db.execute("INSERT INTO user (username, password, admin) VALUES (?, ?, ?)",
               ("user", generate_password_hash("user"), 1))

    for _ in range(10):
        db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                   (fake.name(), fake.password()))
    db.commit()

    for id in range(2, 13):
        db.execute("INSERT INTO post (body, author_id) VALUES (?, ?)", (fake.text(), id))
    db.commit()


@click.command("populate-db")
@with_appcontext
def populate_db_command() -> None:
    """Push fake data to the database."""
    # from flaskr.models import User, Post, Comment
    populate_db()
    click.echo("populated the database.")


def init_app(app: Flask) -> None:
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
