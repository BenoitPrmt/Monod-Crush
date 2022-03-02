from flask import Blueprint, render_template

from flaskr.auth import login_required

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route('/<username>')
def profile(username:str):
    """Show profile of a user"""
    return render_template("/user/profile.html", username=username)

@bp.route('/<username>/edit', methods=("GET", "POST"))
@login_required
def edit(username:str):
    """Edit profile"""
    return render_template("/user/edit.html", username=username)