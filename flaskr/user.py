from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app, g, abort
from werkzeug.security import generate_password_hash

from flaskr.auth_helper import login_required, check_password_strength, check_username
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

    userID = tuple(user)[0]
    print(userID)

    username = request.form["username"]
    firstName = request.form["firstName"]
    bio = request.form["bio"]
    email = request.form["email"]
    class_level = request.form["class_level"]
    class_number = request.form["class_number"]
    instagram = request.form["instagram"]
    twitter = request.form["twitter"]
    github = request.form["github"]
    website = request.form["website"]
    password = request.form["password"]

    error = False

    print(username)
    print(g.user["username"])

    if username != "" and username != g.user["username"]:
        is_valid, msg = check_username(username)
        if not is_valid:
            flash(msg)
            error = True
    

    if password != "":
        is_valid, msg = check_password_strength(password)
        if not is_valid:
            flash(msg)
            error = True
        password = generate_password_hash(password)

    if not error:
        forms = [username, firstName, bio, email, class_level, class_number, instagram, twitter,
                 github, website, password]
        formsName = ["username", "firstName", "bio", "email", "class_level", "class_number", "instagram","twitter",
                "github", "website", "password"]

        # TODO check fields constraints with dict {form: [sqlFormsName, functionToCheck]}

        new_request = "UPDATE user SET "
        c = 0
        args = []
        for form in forms:
            if form != "":
                if form == " " and formsName[c] != "password" and formsName[c] != "username":
                    form = None
                new_request += f", {formsName[c]} = ?"
                args.append(form)
            c += 1

        new_request += f" WHERE id = {userID}"
        new_request = new_request.replace(',', '', 1)

        db.execute(new_request, tuple(args))
        db.commit()

        current_app.logger.info(f"{g.user['id']} ({g.user['username']}) - has edited his profile")

        posts = db.execute("""
        SELECT p.id, p.body, p.status, p.anonymous, p.created, p.author_id, u.username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.author_id = ? AND p.anonymous = 0
        ORDER BY p.created DESC
        """, (user["id"],)
                       ).fetchall()

        return render_template("/user/profile.html", user=user, date=str(date.today()), posts=posts)

    return render_template("/user/edit.html", user=user)


@bp.route("/<username>/delete", methods=["POST"])
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
