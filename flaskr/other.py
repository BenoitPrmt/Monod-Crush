from flask import Blueprint, render_template

bp = Blueprint("other", __name__)


@bp.route('/contact')
def contact():
    """Contact page"""

    return render_template("/other/contact.html")

@bp.route('/about')
def about():
    """About page"""

    return render_template("/other/about.html")