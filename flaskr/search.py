from typing import Union

from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug import Response

from flaskr.db import get_db
from flaskr.models import User

bp = Blueprint("search", __name__)


@bp.route("/search")
def search_user() -> Union[str, Response]:
    """search user and return best result on search_user.html"""

    username = request.args["search_user"]

    if username == "all":  # TODO faire une liste de pseudo interdits comme "staff", "all"
        usernames = User.get_all_username()
        return render_template("search/all_user.html", user=usernames)
    elif username == "staff":
        usernames = User.get_all_username(staff_only=True)
        return render_template("search/all_user.html", user=usernames)
    else:
        try:
            user = User.get_user_by_name(username)
        except ValueError:
            return render_template("error/404_user_not_found.html")
        else:
            return redirect(url_for('user.profile', username=user.username))


@bp.route("/all_user")
def all_user() -> str:
    """ search all user """

    db = get_db()
    user = db.execute("""
        SELECT username
        FROM user 
        WHERE username != 'admin'
        ORDER BY username
        """).fetchall()

    return render_template("search/all_user.html", user=user)
