from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


def get_post(post_id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param post_id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db().execute(
            "SELECT p.id, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (post_id,),
        ).fetchone()
    )

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"] and not g.user["admin"]:
        abort(403)

    return post


@bp.route("/post/new", methods=("GET", "POST"))
@login_required  # TODO autoriser l'utilisateur à créer un post sans être connecté
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        body = request.form["body"]
        error = None

        if not body:
            error = "Le message ne peut pas être vide."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (body, author_id) VALUES (?, ?)",
                (body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/post/<int:post_id>/edit", methods=("GET", "POST"))
@login_required
def edit(post_id: int):
    """Update a post if the current user is the author."""
    post = get_post(post_id)

    if request.method == "POST":
        body = request.form["body"]
        error = None

        if not body:
            error = "Le message ne peut pas être vide."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET , body = ? WHERE id = ?", (body, post_id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/edit.html", post=post)


@bp.route("/post/<int:post_id>/delete", methods=("POST",))
@login_required
def delete(post_id: int):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(post_id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for("blog.index"))
