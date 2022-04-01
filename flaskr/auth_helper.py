import functools
import re
from datetime import datetime, date
from typing import Tuple

from flask import url_for, redirect, g, Blueprint, abort, session

from flaskr.db import get_db

bp = Blueprint('auth_helper', __name__)


@bp.before_app_request
def load_logged_in_user() -> None:
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""

    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT id, username, admin FROM user WHERE id = ?", (user_id,)).fetchone()


def check_password_strength(password: str) -> Tuple[bool, str]:
    """ Check if the password is strong enough """
    # TODO : return one message for all the errors
    # TODO : add check for non alphanumeric characters
    if len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères"
    elif len(password) > 25:
        return False, "Le mot de passe doit contenir 25 caractères maximum"

    return True, ""


def check_username(username: str) -> Tuple[bool, str]:
    """ Check if the username is available """

    if len(username) < 3:
        return False, "Votre nom d'utilisateur doit contenir au moins 3 caractères"
    elif len(username) > 20:
        return False, "Votre nom d'utilisateur doit contenir 20 caractères maximum"
    elif not re.match(r'^[A-Za-z][A-Za-z0-9_-]+$', username):
        return False, "Votre nom d'utilisateur doit commencer par une lettre et peut contenir uniquement des lettres," \
                      " nombres, tirets du bas et tirets"

    db = get_db()
    if db.execute("SELECT 1 FROM user WHERE username = ?", (username,)).fetchone() is not None:
        return False, "Ce nom d'utilisateur est déjà pris"

    return True, ""


def check_date_of_birth(date_of_birth: str) -> Tuple[bool, str]:
    """ Check if the date of birth is valid """
    try:
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    except ValueError:
        return False, "Le format de la date de naissance est invalide"

    if date_of_birth > date.today():
        return False, "Vous voyagez dans le temps ? Votre date de naissance doit être dans le passé"
    elif date_of_birth < date(year=1920, month=1, day=1):
        return False, "Veuillez indiquer une date de naissance valide"

    return True, ""


def login_required(view: callable) -> callable:
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs: dict):
        if g.user is None:
            return redirect(url_for("auth.login"), code=401)

        return view(**kwargs)

    return wrapped_view


def admin_only(view: callable):
    """View decorator that requires an admin user."""

    @functools.wraps(view)
    def wrapped_view(**kwargs: dict):
        if g.user is None or not g.user["admin"]:
            return abort(401)

        return view(**kwargs)

    return wrapped_view
