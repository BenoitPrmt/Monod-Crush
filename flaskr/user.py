from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app
from datetime import date

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

    return render_template("/user/profile.html", user=user, date=str(date.today()))


@bp.route('/<username>/edit')
@login_required
def edit(username: str):
    """Edit profile"""

    # TODO: check if with user id == session id

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    return render_template("/user/edit.html", user=user)


@bp.route("/<username>/edit", methods=["POST"])
@login_required
def update_user(username: str):
    """Update user"""

    current_app.logger.info(f"update user: {username}")
    current_app.logger.debug(f"request.form: {request.form}")

    db = get_db()
    cur = db.cursor()
    user = cur.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    userID = tuple(user)[0]
    print(userID)

    username = request.form["username"]
    firstName = request.form["firstName"]
    bio = request.form["bio"]
    email = request.form["email"]
    class_level = request.form["class_level"]
    class_number = request.form["class_number"]
    instagram = request.form["instagram"]
    facebook = request.form["facebook"]
    linkedin = request.form["linkedin"]
    twitter = request.form["twitter"]
    github = request.form["github"]
    website = request.form["website"]
    password = request.form["password"]

    if password != "":
        password = generate_password_hash(password)

    forms = [username, firstName, bio, email, class_level, class_number, instagram, facebook, linkedin, twitter, github,
             website, password]
    formsName = ["username", "firstName", "bio", "email", "class_level", "class_number", "instagram", "facebook",
                 "linkedin", "twitter", "github", "website", "password"]

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

    print(tuple(args))
    print(new_request)

    db.execute(new_request, tuple(args))
    db.commit()
    return render_template("/user/profile.html", user=user, date=str(date.today()))


@bp.route("/<username>/delete", methods=["POST"])
def delete(username: str):
    """Delete account

    Args:
        username (str): _description_
    """

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    userID = tuple(user)[0]
    print(userID)

    db.execute(f"DELETE FROM user WHERE id = ?", (userID,))
    db.commit()
    session.clear()
    return redirect(url_for("blog.index"))
