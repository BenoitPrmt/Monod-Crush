from typing import Union

from flask import Blueprint, flash, g, redirect, render_template, request, url_for, Response, current_app, abort, \
    jsonify

from flaskr.auth_decorator import login_required
from flaskr.models import Post

bp = Blueprint("blog", __name__)


@bp.route("/")
def index() -> str:
    """Show all the posts, most recent first."""

    return render_template("blog/index.html", posts=Post.get_posts())


@bp.route("/post/new", methods=("GET", "POST"))
@login_required
def create() -> Union[str, Response]:
    """Create a new post for the current user."""

    if request.method == "POST":
        message = request.form["body"]
        anonymous = request.form.get("anonymous", "off")

        if anonymous not in ("on", "off"):
            abort(400)
            error = True
        else:
            anonymous = anonymous == "on"

        try:
            post = Post.create(message, g.user.id, anonymous)
        except ValueError as e:
            flash(str(e), "warning")

        else:
            current_app.logger.info(f"{g.user.id} ({g.user.username}) - created a new post with id {post.id}")

            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/post/<int:post_id>/edit", methods=("GET", "POST"))
@login_required
def edit(post_id: int) -> Union[str, Response]:
    """Update a post if the current user is the author."""

    post = Post.get_post_or_404(post_id)

    if request.method == "POST":
        message = request.form["body"]

        try:
            post.update(message)
        except ValueError as e:
            flash(str(e), "warning")
        else:
            current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - updated post {post_id}")

            return redirect(url_for("blog.index"))

    return render_template("blog/edit.html", post=post)


@bp.route("/post/<int:post_id>/like", methods=["POST"])
@login_required
def toggle_like(post_id: int):
    """ Like a post. """
    post = Post.get_post_or_404(post_id, check_user_is_owner=False)

    if g.user.id in post.liked_by:
        post.unlike(g.user.id)
    else:
        post.like(g.user.id)

    post = Post.get_post(post_id)

    return jsonify({"success": True, "likes": len(post.liked_by)})


@bp.route("/post/<int:post_id>/unlike", methods=["POST"])
@login_required
def unlike(post_id: int):
    """ Like a post. """
    post = Post.get_post_or_404(post_id, check_user_is_owner=False)

    post.unlike(g.user.id)

    post = Post.get_post(post_id)

    return jsonify({"likes": len(post.liked_by)})


@bp.route("/post/<int:post_id>/report", methods=["POST"])
@login_required
def report(post_id: int) -> Response:
    """Report a post."""

    post = Post.get_post_or_404(post_id)

    if g.user.id in post.reported_by:
        return jsonify({"success": False, "message": "You have already reported this post."})

    else:
        post.report(g.user.id)
        return jsonify({"success": True})  # TODO: reload the page to hide if it is third report


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id: int) -> Response:
    """Delete a post."""

    post = Post.get_post_or_404(post_id)

    post.delete()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - deleted post {post_id}")

    return jsonify({"success": True})


@bp.route("/post/latest")
def latest() -> Response:
    """Return the latest posts."""
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
