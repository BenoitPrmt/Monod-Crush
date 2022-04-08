import functools
from typing import Union

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, Response, current_app, g, \
    abort

from flaskr.auth_decorator import login_required
from flaskr.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user() -> None:
    """If a user id is stored in the session, load the user object from the database into ``g.user``."""

    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.get_user_by_id(user_id)


@bp.route("/register", methods=["GET", "POST"])
def register() -> Union[Response, str]:
    """Register a new user. """
    if request.method == "POST":

        username = request.form["username"]
        date_of_birth = request.form["date_of_birth"]
        password = request.form["password"]

        try:
            user = User.create(username=username, date_of_birth=date_of_birth, password=password)
        except ValueError as e:
            flash(str(e), "warning")
        else:
            session.clear()
            session["user_id"] = user.id

            current_app.logger.info(f"{user.id} ({user.username}) - registered, welcome!")

            return redirect(url_for("blog.index"))

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> Union[Response, str]:
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            user = User.login(username=username, password=password)
        except ValueError as e:
            flash(str(e), "error")

        else:
            session.clear()
            session["user_id"] = user.id

            current_app.logger.info(f"{user.id} ({user.username}) - logged in")

            return redirect(url_for("blog.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout() -> Response:
    """ Clear the current session """

    session.clear()

    current_app.logger.info(f"{g.user.id} ({g.user.username}) - logged out")

    return redirect(url_for("blog.index"))



