from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app, g
from datetime import date

from werkzeug.security import generate_password_hash
from flaskr.auth_helper import login_required, check_password_strength, check_username
from flaskr.db import get_db

bp = Blueprint("user", __name__, url_prefix="/user") #a faire jspl quoi mettre dedans

@bp.route("/search", methods=("GET"))
def serach_user():
    """search user and return best result on search_user.html"""
    

    return render_template("search/search_user.html")