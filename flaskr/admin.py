from flask import Blueprint, g, redirect, render_template, url_for, Response, current_app, request

from flaskr.auth_helper import admin_only
from flaskr.blog_helper import get_post
from flaskr.db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route('/')
@admin_only
def panel() -> str:
    """Show admin panel"""

    db = get_db()
    users = db.execute("SELECT COUNT(id) FROM user").fetchone()
    admins = db.execute("SELECT COUNT(id) FROM user WHERE admin = 1").fetchone()
    nb_posts = db.execute("SELECT COUNT(id) FROM post").fetchone()
    comments = db.execute("SELECT COUNT(id) FROM comment").fetchone()
    posts = db.execute("""
        SELECT p.id, p.body, p.status,p.anonymous, p.created, p.author_id, u.username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.reported != ''
        ORDER BY p.created DESC
        
        """).fetchall()
    print(posts)
    return render_template("/admin/panel.html", nb_posts=nb_posts[0], users=users[0],
                           admins=admins[0], comments=comments[0], posts=posts)


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@admin_only
def delete(post_id: int) -> Response:
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(post_id, check_author=False)

    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (post_id,))
    db.commit()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - deleted post {post_id}")

    return redirect(url_for("admin.panel"))


@bp.route("/post/<int:post_id>/checking", methods=["POST"])
@admin_only
def checking(post_id: int) -> Response:
    get_post(post_id, check_author=False)

    db = get_db()
    r = db.execute("SELECT reported, status FROM post WHERE id = ?", (post_id,)).fetchone()
    db.execute("UPDATE post SET reported = NULL WHERE id = ?", (post_id,)).fetchone()

    if r["status"] == "hidden":
        db.execute("UPDATE post SET status = 'visible' WHERE id = ?", (post_id,))

    db.commit()
    return redirect(url_for("admin.panel"))

@bp.route("user/<username>/add")
@admin_only
def ajout_admin(username):
    db = get_db()
    db.execute(
        "UPDATE user SET admin = 1 WHERE username = ?", (username,)).fetchone()
    db.commit()
    return redirect(url_for('user.profile', username=username))

@bp.route("user/<username>/sup")
@admin_only
def supprimer_admin(username):
    db = get_db()
    db.execute(
        "UPDATE user SET admin = 0 WHERE username = ?", (username,)).fetchone()
    db.commit()
    return redirect(url_for('user.profile', username=username))

