from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from datetime import date

from werkzeug.security import generate_password_hash
from flaskr.auth_helper import login_required, check_password_strength, check_username
from flaskr.db import get_db

bp = Blueprint("user", __name__, url_prefix="/user")

today = date.today()


@bp.route('/<username>')
@login_required
def profile(username: str):
    """Show profile of a user"""

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    return render_template("/user/profile.html", user=user, date=today)


@bp.route('/<username>/edit', methods=("GET", "POST"))
@login_required
def edit(username: str):
    """Edit profile"""

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    return render_template("/user/edit.html", user=user)

# @bp.route("/<username>/edit", methods=("GET", "POST"))
def update_user(username:str):
    """Update user"""

    print("update_user")

    db = get_db()

    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    username = request.form["username"]
    firstName = request.form["firstName"]
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

    db.execute(
        """UPDATE user
        SET username = ?, firstName = ?, email = ?, class_level = ?, class_number = ?, instagram = ?, facebook = ?, linkedin = ?, twitter = ?, github = ?, website = ?, password = ?
        WHERE id = ?""",
        (username, firstName, email, class_level, class_number, instagram, facebook, linkedin, twitter, github, website, generate_password_hash(password), user.id),
    )
    db.commit()
    db.close()
    return render_template("/user/profile.html", user=user, date=today)