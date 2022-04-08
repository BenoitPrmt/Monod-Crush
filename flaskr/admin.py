from flask import Blueprint, g, redirect, render_template, url_for, Response, current_app, jsonify, request

from flaskr.auth_decorator import admin_only
from flaskr.db import get_db
from flaskr.models import Post, User

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route('/')
@admin_only
def panel() -> str:
    """Show admin panel with stats and reports posts"""

    db = get_db()
    users = db.execute("SELECT COUNT(id) FROM user").fetchone()
    banned = db.execute("SELECT COUNT(id) FROM user WHERE accreditation = 0").fetchone()  # TODO group by
    moderators = db.execute("SELECT COUNT(id) FROM user WHERE accreditation = 2").fetchone()  # TODO Unused variable
    admins = db.execute("SELECT COUNT(id) FROM user WHERE accreditation = 3").fetchone()
    nb_posts = db.execute("SELECT COUNT(id) FROM post").fetchone()
    comments = db.execute("SELECT COUNT(id) FROM comment").fetchone()
    likes = db.execute("SELECT COUNT(*) FROM like").fetchone()

    posts_reported = Post.get_posts_for_moderation()
    return render_template("/admin/panel.html", nb_posts=nb_posts[0], likes =likes[0], users=users[0],
                           admins=admins[0], comments=comments[0], posts=posts_reported)


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@admin_only
def delete(post_id: int) -> Response:
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = Post.get_post_or_404(post_id, check_user_is_owner=False)

    post.delete()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - deleted post {post_id}")

    return jsonify({"success": True})


@bp.route("/post/<int:post_id>/checking", methods=["POST"])
@admin_only
def checking(post_id: int) -> Response:
    """Check a post."""

    post = Post.get_post_or_404(post_id, check_user_is_owner=False)
    post.clear_report()
    post.show()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - checked post {post_id}")

    return jsonify({"success": True})


@bp.route("user/<username>/set_admin")
@admin_only
def add_admin(username: str) -> Response:
    """set user as admin"""
    user = User.get_user_by_id_or_404(username)
    user.promote(3)
    return redirect(url_for('user.profile', username=username))


@bp.route("user/<username>/remove_admin")
@admin_only
def remove_admin(username: str) -> Response:
    """remove admin rights from user"""
    user = User.get_user_by_id_or_404(username)
    user.promote(2)
    return redirect(url_for('user.profile', username=username))

# TODO: add ban user
# @bp.route("user/<username>/ban")
# @admin_only
# def remove_admin(username: str) -> Response:
#     """remove admin rights from user"""
#     user = User.get_user_by_id_or_404(username)
#     user.ban()
#     return redirect(url_for('user.profile', username=username))
