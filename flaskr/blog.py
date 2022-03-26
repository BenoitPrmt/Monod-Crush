import locale
from typing import Union

from flask import Blueprint, flash, g, redirect, render_template, request, url_for, Response, current_app

from flaskr.auth_helper import login_required
from flaskr.blog_helper import get_post, check_message_body
from flaskr.db import get_db

bp = Blueprint("blog", __name__)

# set locale date format to french
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


@bp.route("/")
def index() -> str:
    """Show all the posts, most recent first."""

    db = get_db()
    posts = db.execute("""
        SELECT p.id, p.body, p.status,p.anonymous, p.created, p.author_id, u.username
        FROM post p JOIN user u ON p.author_id = u.id
        ORDER BY p.created DESC
        """).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/post/new", methods=("GET", "POST"))
@login_required  # TODO autoriser l'utilisateur à créer un post sans être connecté
def create() -> Union[str, Response]:
    """Create a new post for the current user."""
    if request.method == "POST":
        body = request.form["body"]
        anonymous = request.form.get("anonymous", "off")
        error = False

        is_valid, msg = check_message_body(body)
        if not is_valid:
            flash(msg)
            error = True

        if anonymous not in ("on", "off"):
            flash("invalid anonymous value")
            error = True
        else:
            anonymous = anonymous == "on"

        if not error:
            db = get_db()
            r = db.execute(
                "INSERT INTO post (body, author_id, anonymous) VALUES (?, ?, ?)",
                (body, g.user["id"], anonymous)
            )
            db.commit()

            current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - created a new post with id {r.lastrowid}")

            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/post/<int:post_id>/edit", methods=("GET", "POST"))
@login_required
def edit(post_id: int) -> Union[str, Response]:
    """Update a post if the current user is the author."""
    post = get_post(post_id)

    if request.method == "POST":
        body = request.form["body"]
        # anonymous = request.form["anonymous"]
        error = False

        is_valid, msg = check_message_body(body)
        if not is_valid:
            flash(msg)
            error = True

        # TODO add in html checkbox
        # if anonymous not in ("on", "off"):
        #     flash("invalid anonymous value")
        #     error = True
        # else:
        #     anonymous = anonymous == "on"

        # TODO reset status Check after edit

        if not error:
            db = get_db()
            db.execute("UPDATE post SET body = ? WHERE id = ?", (body, post_id))
            db.commit()

            current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - edited post {post_id}")

            return redirect(url_for("blog.index"))

    return render_template("blog/edit.html", post=post)


@bp.route("/post/<int:post_id>/report", methods=["POST"])
@login_required
def report(post_id: int) -> Response:
    """Report a post.

    Ensures that the post exists and that the logged-in user is the
    author of the post.
    """
    get_post(post_id, check_author=False)

    db = get_db()
    r = db.execute("SELECT reported, status FROM post WHERE id = ?", (post_id,)).fetchone()
    if r["reported"] is not None:
        reports = r["reported"].split(",")
    else:
        reports = []

    if str(g.user["id"]) in reports:
        flash("You have already reported this post.")
        return redirect(url_for("blog.index"))

    # status : visible, hidden, checked
    if r["status"] == "visible":

        reports.append(str(g.user["id"]))
        db.execute("UPDATE post SET reported = ? WHERE id = ?", (",".join(reports), post_id))
        if len(reports) >= 3:
            db.execute("UPDATE post SET status = 'hidden' WHERE id = ?", (post_id,))
        db.commit()

        current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - reported post {post_id}")

    return redirect(url_for("blog.index"))


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id: int) -> Response:
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(post_id)

    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (post_id,))
    db.commit()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - deleted post {post_id}")

    return redirect(url_for("blog.index"))
