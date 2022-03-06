import functools
from typing import Union

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug import Response
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def admin(view):
    """View decorator that requires an admin user."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user["admin"] == 0:
            return redirect(url_for("blog.index"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register() -> Union[Response, str]:
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        dateOfBirth = request.form["dateOfBirth"]
        password = request.form["password"]
        db = get_db()
        error = None

        # check if username is valid
        if not username:
            error = "Choisissez un nom d'utilisateur !"
        elif not 3 < len(username) < 26:
            error = "Le nom d'utilisateur doit contenir entre 4 et 25 caractères."
        elif not username.isalpha():
            error = "Le nom d'utilisateur ne peut pas contenir de chiffres ni de symboles !"

        # check date of birth
        elif not dateOfBirth:
            # TODO : check if date is valid regex
            error = "Indiquez votre date de naissance !."

        # check password
        elif not password:
            error = "Remplissez le champ mot de passe."
        elif not 5 < len(password) < 26:
            error = "Le mot de passe doit contenir entre 6 et 25 caractères."

        if error is None:
            try:
                db.execute("INSERT INTO user (username, dateOfBirth, password) VALUES (?, ?, ?)",
                           (username, dateOfBirth, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"Le nom d'utilisateur {username} est deja pris."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> Union[Response, str]:
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Nom d'utilisateur incorrect"
        elif not check_password_hash(user["password"], password):
            error = "Mot de passe incorrect"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout() -> Response:
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
