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
        print(users)
        return render_template("search/search_user.html", user="None")
    else:
        print(users)
        return render_template("search/search_user.html", user=username)
