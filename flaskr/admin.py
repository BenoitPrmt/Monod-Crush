from flask import Blueprint, render_template

from flaskr.auth_helper import admin_only
from flaskr.db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route('/')
@admin_only
def panel() -> str:
    """Show admin panel"""

    db = get_db()
    users = db.execute("SELECT COUNT(id) FROM user").fetchone()
    admins = db.execute("SELECT COUNT(id) FROM user WHERE admin = 1").fetchone()
    posts = db.execute("SELECT COUNT(id) FROM post").fetchone()
    comments = db.execute("SELECT COUNT(id) FROM comment").fetchone()

    return render_template("/admin/panel.html", posts=posts[0], users=users[0],
                           admins=admins[0], comments=comments[0])
