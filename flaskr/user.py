from flask import Blueprint, render_template

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route('/<username>') #<str:username> g.user['username']
def profile(username:str):
    """Show profile of a user"""
    return render_template("/user/profile.html", username=username)