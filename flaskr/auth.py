from typing import Union

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, Response, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.auth_helper import check_password_strength, check_username, check_date_of_birth, login_required
from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register() -> Union[Response, str]:
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":

        username = request.form["username"]
        dateOfBirth = request.form["dateOfBirth"]
        password = request.form["password"]

        error = False

        is_valid, msg = check_username(username)
        if not is_valid:
            flash(msg, "warning")
            error = True

        is_valid, msg = check_date_of_birth(dateOfBirth)
        if not is_valid:
            flash(msg, "warning")
            error = True

        is_valid, msg = check_password_strength(password)
        if not is_valid:
            flash(msg, "warning")
            error = True

        if not error:
            db = get_db()
            r = db.execute(
                "INSERT INTO user (username, dateOfBirth, password) VALUES (?, ?, ?)",
                (username, dateOfBirth, generate_password_hash(password)),
            )
            db.commit()
            # auto login after registration
            session["user_id"] = r.lastrowid

            current_app.logger.info(f"{r.lastrowid} ({username}) - registered, welcome!")

            return redirect(url_for("blog.index"))

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> Union[Response, str]:
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = False

        if not username and not password:
            error = True
        else:
            db = get_db()
            user = db.execute(
                "SELECT password, id FROM user WHERE username = ?", (username,)
            ).fetchone()
            if user is None:
                error = True
            elif not check_password_hash(user["password"], password):
                error = True

        if error:
            flash("Nom d'utilisateur ou mot de passe incorrect", "error")
        else:
            session.clear()  # TODO : clear only the user_id
            session["user_id"] = user["id"]

            import os
            current_app.logger.info(f"{user['id']} ({username}) - logged in le pc de {os.getenv('COMPUTERNAME')}")

            return redirect(url_for("blog.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout() -> Response:
    """Clear the current session, including the stored user id."""
    session.clear()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - logged out")

    return redirect(url_for("blog.index"))
