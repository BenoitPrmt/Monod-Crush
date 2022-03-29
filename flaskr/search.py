from flask import Blueprint, render_template, request

from flaskr.db import get_db


bp = Blueprint("search", __name__)


@bp.route("/search")
def search_user() -> str:
    """search user and return best result on search_user.html"""

    db = get_db()
    username = request.args["search_user"]

    users = db.execute("SELECT admin FROM user WHERE username = ?", (username,)).fetchone()
    if users is None:
        return render_template("error/404_user_not_found.html")
    else:
        return render_template("search/search_user.html", user=username)

@bp.route("/all_user")
def all_user():
    db = get_db()
    user = db.execute("""
        SELECT username
        FROM user 
        WHERE username != 'admin'
        ORDER BY username
        """).fetchall()
    
    print(user)
    return render_template("search/all_user.html", user=user)
    
