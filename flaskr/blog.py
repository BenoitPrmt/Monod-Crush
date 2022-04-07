from typing import Union

from flask import Blueprint, flash, g, redirect, render_template, request, url_for, Response, current_app, abort, \
    jsonify

from flaskr.auth_helper import login_required, admin_only
from flaskr.blog_helper import get_post, check_message_body, moderate_message_body
from flaskr.db import get_db
from flaskr.sql_helper import UserSet
from flaskr.insta_content_generator import generate_pic

bp = Blueprint("blog", __name__)


@bp.route("/")
def index() -> str:
    """Show all the posts, most recent first."""

    db = get_db()
    posts = db.execute("""
        SELECT p.id, p.body, p.status, p.reported, p.anonymous, p.created,
        count_users(p.like) AS nb_likes, like, p.author_id, u.username
        FROM post p JOIN user u ON p.author_id = u.id
        ORDER BY p.created DESC""").fetchall()

    return render_template("blog/index.html", posts=posts, UserSet=UserSet)


@bp.route("/post/<int:post_id>/like", methods=["POST"])
@login_required
def like(post_id: int):
    """ Like a post. """
    get_post(post_id, check_author=False)

    db = get_db()
    r = db.execute("SELECT like FROM post WHERE id = ?", (post_id,)).fetchone()

    likes = UserSet(r["like"])

    likes.toggle(g.user["id"])
    print(likes)

    db.execute("UPDATE post SET like = ? WHERE id = ?", (likes.join(), post_id,))
    db.commit()

    return jsonify({"likes": len(likes), "my": g.user["id"] in likes})


@bp.route("/post/<int:post_id>/insta", methods=["POST"])
@admin_only
def insta(post_id: int):
    """ Like a post. """
    post = get_post(post_id, check_author=False)

    try :
        generate_pic(post["body"])
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"error": str(e)}), 500


    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - instagram post {post_id}")

    return "OK", 201


@bp.route("/post/new", methods=("GET", "POST"))
@login_required
def create() -> Union[str, Response]:
    """Create a new post for the current user."""
    if request.method == "POST":
        body = request.form["body"]
        anonymous = request.form.get("anonymous", "off")
        error = False

        if anonymous not in ("on", "off"):
            abort(400)
            error = True
        else:
            anonymous = anonymous == "on"

        is_valid, msg = check_message_body(body)
        if not is_valid:
            flash(msg, "warning")
            error = True

        if not error:
            # Moderate the content message
            body = moderate_message_body(body)

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
        error = False

        is_valid, msg = check_message_body(body)
        if not is_valid:
            flash(msg, "warning")
            error = True

        # TODO reset status Check after edit

        if not error:
            # Moderate the content message
            body = moderate_message_body(body)

            db = get_db()
            db.execute("UPDATE post SET body = ? WHERE id = ?", (body, post_id))
            db.commit()

            current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - edited post {post_id}")

            return redirect(url_for("blog.index"))

    return render_template("blog/edit.html", post=post)


@bp.route("/post/<int:post_id>/report", methods=["POST"])
@login_required
def report(post_id: int) -> Response:
    """Report a post."""
    get_post(post_id, check_author=False)

    db = get_db()
    r = db.execute("SELECT reported, status FROM post WHERE id = ?", (post_id,)).fetchone()

    reports = UserSet(r["reported"])

    if g.user["id"] in reports:
        flash("Vous avez déjà signalé ce post")
        return redirect(url_for("blog.index"))

    # status : visible, hidden, checked
    if r["status"] == "visible":

        reports.add(g.user["id"])
        db.execute("UPDATE post SET reported = ? WHERE id = ?", (reports.join(), post_id))

        flash("Post signalé")
        current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - reported post {post_id}")

        if len(reports) >= 1:
            db.execute("UPDATE post SET status = 'hidden' WHERE id = ?", (post_id,))
            current_app.logger.info(f"post {post_id} is now hidden")
        db.commit()

    return redirect(url_for("blog.index"))


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id: int) -> Response:
    """Delete a post."""
    get_post(post_id)

    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (post_id,))
    db.commit()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - deleted post {post_id}")

    return redirect(url_for("blog.index"))


@bp.route("/post/latest")
def latest() -> Response:
    """Return the latest posts."""
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
