from flask import Blueprint, render_template
from datetime import date

from flaskr.auth_helper import login_required
from flaskr.db import get_db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/<username>')
@login_required
def profile(username: str):
    """Show profile of a user"""

    today = date.today()

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    return render_template("/user/profile.html", user=user, date=today)


@bp.route('/<username>/edit', methods=("GET", "POST"))
@login_required
def edit(username: str):
    """Edit profile"""

    return render_template("/user/edit.html", username=username)    