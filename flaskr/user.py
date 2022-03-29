from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app, g, abort

from flaskr.auth_helper import login_required, check_username
from flaskr.db import get_db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/<username>')
def profile(username: str):
    """Show profile of a user"""

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        return render_template("error/404_user_not_found.html", username=username)

    posts = db.execute("""
        SELECT p.id, p.body, p.status, p.anonymous, p.created, p.author_id, u.username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.author_id = ? AND p.anonymous = 0
        ORDER BY p.created DESC
        """, (user["id"],)
                       ).fetchall()

    return render_template("/user/profile.html", user=user, date=str(date.today()), posts=posts)


@bp.route('/<username>/edit')
@login_required
def edit(username: str):
    """Edit profile"""

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None or user["id"] != g.user["id"]:
        abort(403)  # Forbidden

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
        abort(403)  # Forbidden

    # {"sql_row_name and form_name", function_to_check_input}
    form = {
        "username": check_username,
        # "email": check_email,
        # "firstName": check_firstName,
        # "bio": check_bio,
        # "class_level": check_class_level,
        # "class_number": check_class_number,
        # "instagram": check_instagram,
        # "twitter": check_twitter,
        # "github": check_github,
        # "website": check_website,
    }

    sql_rows_name = []
    rows_values = []

    for form_name, check_function in form.items():

        form_value = request.form[form_name]

        # if the value is the same that the one in the database, skip
        if form_value == user[form_name]:
            continue

        # check if all the values are valid
        is_valid, error_message = check_function(request.form[form_name])
        if not is_valid:
            flash(error_message)
            return render_template("/user/edit.html", user=user)

        rows_values.append(request.form[form_name])
        sql_rows_name.append(f"{form_name} = ?")

    if len(sql_rows_name) == 0:
        # if there is no change, redirect to the profile
        flash("Aucune modification n'a été effectuée", "info")
        return redirect(url_for("user.profile", username=username))

    rows_values.append(user["id"])

    db.execute(f"UPDATE user SET {', '.join(sql_rows_name)} WHERE id = ?", rows_values)
    db.commit()

    current_app.logger.info(
        f"{g.user['id']} ({g.user['username']}) - has edited his profile ({sql_rows_name})")  # TODO remove '= ?'

    flash("Your profile has been updated!", "success")
    return redirect(url_for("user.profile", username=request.form.get("username", user["username"])))


@bp.route("/<username>/delete", methods=["POST"])
@login_required
def delete(username: str):
    """Delete account

    Args:
        username (str): _description_
    """

    # TODO: check if with user is owner of the account
    # TODO: @login_required
    # html post request
    # doesn't work
    # check return in alert

    db = get_db()
    user = db.execute(
        "SELECT id FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None or user["id"] != g.user["id"]:
        abort(403)  # Forbidden

    db.execute(f"DELETE FROM user WHERE id = ?", (user["id"],))
    db.commit()

    session.clear()

    current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - has deleted his account, bye bye")

    return redirect(url_for("blog.index"))
