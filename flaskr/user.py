from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app, g, abort, \
    Response

from flaskr.auth_decorator import login_required
from flaskr.db import get_db
from flaskr.models import User, Post
from flaskr.user_helper import check_email, check_firstname, check_bio, check_class_level, check_class_number, \
    check_social, check_website

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/<username>')
def profile(username: str):
    """Show profile of a user"""

    user = User.get_user_by_name_or_404(username)
    user_info = user.get_full_info()

    current_app.logger.info(f"has viewed his profile ({user_info})")

    posts = Post.get_posts_by_user(user.id)

    return render_template("/user/profile.html", user=user_info, today=date.today(), posts=posts)


@bp.route('/<username>/edit')
@login_required
def edit(username: str):
    """Edit profile"""

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None or user["id"] != g.user["id"]:
        abort(401)  # Unauthorized

    return render_template("/user/edit.html", user=user)


@bp.route("/<username>/edit", methods=["POST"])
@login_required
def update_user(username: str):
    """Update user"""

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None or user["username"] != g.user["username"]:
        abort(401)  # Unauthorized

    # {"sql_row_name and form_name", function_to_check_input}
    form = {
        "username": check_username,
        "email": check_email,
        "firstName": check_firstname,
        "bio": check_bio,
        "class_level": check_class_level,
        "class_number": check_class_number,
        "instagram": check_social,
        "twitter": check_social,
        "github": check_social,
        "website": check_website,
    }

    sql_column_name = []
    sql_values = []

    for form_name, check_function in form.items():

        form_value = request.form[form_name]

        if form_value == "":
            continue

        # if the value is the same that the one in the database, skip
        if form_value == user[form_name]:
            continue

        # check if all the values are valid
        is_valid, error_message = check_function(request.form[form_name])
        if not is_valid:
            flash(error_message, "warning")
            return render_template("/user/edit.html", user=user)

        sql_values.append(request.form[form_name])
        sql_column_name.append(f"{form_name} = ?")

    if len(sql_column_name) == 0:
        # if there is no change, redirect to the profile
        flash("Aucune modification n'a été effectuée", "info")
        return redirect(url_for("user.profile", username=username))

    sql_values.append(user["id"])

    db.execute(f"UPDATE user SET {', '.join(sql_column_name)} WHERE id = ?", sql_values)
    db.commit()

    current_app.logger.info(
        f"{g.user['id']} ({g.user['username']}) - has edited his profile ({sql_column_name})")  # TODO remove '= ?'

    flash("Your profile has been updated!", "success")
    return redirect(url_for("user.profile", username=request.form.get("username", user["username"])))


@bp.route("/<username>/delete", methods=["POST"])
@login_required
def delete(username: str) -> Response:
    """Delete account

    Args:
        username (str): username of the user to delete
    """

    db = get_db()
    user = db.execute(
        "SELECT id, admin FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        abort(404)  # Not found

    if user["id"] == g.user["id"]:
        db.execute(f"DELETE FROM user WHERE id = ?", (user["id"],))
        db.commit()

        session.clear()

        current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - has deleted his account, bye bye")

        return redirect(url_for("index"))

    elif g.user["admin"]:

        # an admin can delete any admin account
        if user["admin"]:
            abort(403)  # Forbidden

        db.execute(f"DELETE FROM user WHERE id = ?", (user["id"],))
        db.commit()

        current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - has deleted {user['id']} ({username})")

        return redirect(url_for("admin.panel"))
    else:
        abort(403)  # Forbidden
