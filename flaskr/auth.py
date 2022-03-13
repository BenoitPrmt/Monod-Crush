from typing import Union

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, Response
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.auth_helper import check_password_strength, check_username, check_date_of_birth
from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register")
def register() -> str:
    return render_template("auth/register.html")


@bp.route("/register", methods=["POST"])
def post_register() -> Union[Response, str]:
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    username = request.form["username"]
    dateOfBirth = request.form["dateOfBirth"]
    password = request.form["password"]

    db = get_db()
    error = False

    is_valid, msg = check_username(username)
    if not is_valid:
        flash(msg)
        error = True

    is_valid, msg = check_date_of_birth(dateOfBirth)
    if not is_valid:
        flash(msg)
        error = True

    is_valid, msg = check_password_strength(password)
    if not is_valid:
        flash(msg)
        error = True

    if error:
        return render_template("auth/register.html")
    else:
        r = db.execute(
            "INSERT INTO user (username, dateOfBirth, password) VALUES (?, ?, ?)",
            (username, dateOfBirth, generate_password_hash(password)),
        )
        db.commit()
        # auto login after registration
        session["user_id"] = r.lastrowid
        return redirect(url_for("blog.index"))


@bp.route("/login", methods=("GET", "POST"))
def login() -> Union[Response, str]:
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None
        user = db.execute(
            "SELECT password, id FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Nom d'utilisateur incorrect"
        elif not check_password_hash(user["password"], password):
            error = "Mot de passe incorrect"

        if error:
            flash(error)
        else:
            session.clear()  # TODO : clear only the user_id
            session["user_id"] = user["id"]
            return redirect(url_for("blog.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout() -> Response:
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("blog.index"))
