import functools
from flask import url_for, g, abort, redirect


def login_required(view: callable) -> callable:
    """View decorator that redirects anonymous users to the login page."""

    # noinspection PyMissingOrEmptyDocstring
    @functools.wraps(view)
    def wrapped_view(**kwargs: dict):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def moderator_only(view: callable):
    """View decorator that requires an admin user."""

    # noinspection PyMissingOrEmptyDocstring
    @functools.wraps(view)
    def wrapped_view(**kwargs: dict):
        if g.user is None:
            return redirect(url_for("auth.login"))
        elif g.user.accreditation not in ("admin", "moderator"):
            abort(403)

        return view(**kwargs)

    return wrapped_view


def admin_only(view: callable):
    """View decorator that requires an admin user."""

    # noinspection PyMissingOrEmptyDocstring
    @functools.wraps(view)
    def wrapped_view(**kwargs: dict):
        if g.user is None:
            return redirect(url_for("auth.login"))
        elif g.user.accreditation != 3:
            abort(403)

        return view(**kwargs)

    return wrapped_view
