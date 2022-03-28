from re import search
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app, g
from datetime import date

from werkzeug.security import generate_password_hash
from flaskr.auth_helper import login_required, check_password_strength, check_username
from flaskr.db import get_db

bp = Blueprint("search", __name__) #a faire jspl quoi mettre dedans

@bp.route("/search")
def search_user():
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