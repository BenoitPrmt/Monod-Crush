from flask import Blueprint, render_template

bp = Blueprint("instamap", __name__)


@bp.route('/map')
def map():
    """Map page"""

    return render_template("/instamap/instamap.html")