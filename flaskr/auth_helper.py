import functools
import re
from datetime import datetime
from typing import Tuple

from flask import url_for, redirect, g, Blueprint, abort, session

from flaskr.db import get_db

bp = Blueprint('auth_helper', __name__)


@bp.before_app_request
def load_logged_in_user() -> None:
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""

    # g.t = time.time()
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        # get information for header
        g.user = get_db().execute("SELECT id, username, admin FROM user WHERE id = ?", (user_id,)).fetchone()
    # current_app.logger.debug(f"g.user : {g.user}, time : {time.time() - g.t}")


# @bp.after_app_request
# def after_request(response: Response) -> Response:
#     """ Profile the response time of the request. If in debug mode"""
#     current_app.logger.debug(f"request response time: {time.time() - g.t}, response : {request.path}")
#     # TODO : add the response time to the log and store it in db for analysis
#     return response


def check_password_strength(password: str) -> Tuple[bool, str]:
    """ Check if the password is strong enough """
    # TODO : return one message for all the errors
    # TODO : add check for non alphanumeric characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    elif len(password) > 25:
        return False, "Password must be at most 25 characters long"
    elif password.isalpha():  # only alphabets
        return False, "Password must contain at least one number"
    elif password.islower():  # only lowercase
        return False, "Password must contain at least one uppercase letter"
    elif password.isupper():  # only uppercase
        return False, "Password must contain at least one lowercase letter"

    return True, ""


def check_username(username: str) -> Tuple[bool, str]:
    """ Check if the username is available """

    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    elif len(username) > 20:
        return False, "Username must be at most 20 characters long"
    elif not re.match(r'^[A-Za-z][A-Za-z0-9_-]+$', username):
        return False, "Username must start with a letter and contain only letters, numbers, underscores and dashes"

    db = get_db()
    if db.execute("SELECT 1 FROM user WHERE username = ?", (username,)).fetchone() is not None:
        return False, "Username already taken"

    return True, ""


def check_date_of_birth(date_of_birth: str) -> Tuple[bool, str]:
    """ Check if the date of birth is valid """
    try:
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date of birth format"

    if date_of_birth > datetime.now():
        return False, "Date of birth must be in the past"
    elif date_of_birth < datetime(year=1920, month=1, day=1):
        return False, "Give your real date of birth"

    return True, ""


def login_required(view: callable) -> callable:
    """View decorator that redirects anonymous users to the login page."""

    # noinspection PyMissingOrEmptyDocstring
    @functools.wraps(view)
    def wrapped_view(**kwargs: dict):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def admin_only(view: callable):
    """View decorator that requires an admin user."""

    # noinspection PyMissingOrEmptyDocstring
    @functools.wraps(view)
    def wrapped_view(**kwargs: dict):
        if g.user is None or not g.user["admin"]:
            return abort(403)

        return view(**kwargs)

    return wrapped_view
