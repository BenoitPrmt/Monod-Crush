from flask import Blueprint, redirect, render_template, request, url_for

from flaskr.db import get_db

bp = Blueprint("search", __name__)


@bp.route("/search")
def search_user() -> str:
    """search user and return best result on search_user.html"""

    db = get_db()
    username = request.args["search_user"]

    users = db.execute("SELECT admin FROM user WHERE username = ?", (username,)).fetchone()

    
    if username == "admin":
        username = db.execute("""
        SELECT username
        FROM user 
        WHERE admin = 1
        ORDER BY username
        """).fetchall()
        return render_template("search/all_user.html", user=username)
    
    elif username == "all":
        user = db.execute("""
        SELECT username
        FROM user 
        WHERE username != 'admin'
        ORDER BY username
        """).fetchall()
        return render_template("search/all_user.html", user=user)

    elif users is None:
        return render_template("error/404_user_not_found.html")

    else:
        return redirect(url_for('user.profile', username=username))


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
