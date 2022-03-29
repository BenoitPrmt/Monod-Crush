from flask import render_template, current_app, request, redirect, g
from werkzeug.exceptions import HTTPException


def get_user_or_ip() -> str:
    """
    Returns the user or the IP address of the client
    """
    if g.user is not None:
        return f"{g.user['id']} ({g.user['username']})"

    return request.headers.get('X-Real-IP', request.remote_addr)


def error_handler(error: HTTPException):
    """ Error handler for HTTP exceptions. """

    # redirect foo/bar/something/  to foo/bar/something
    # check if not end with foo/bar////////// for not enter in loop
    if error.code == 404 and request.path.endswith('/') and not request.path.endswith('//'):
        return redirect(request.path[:-1])

    elif error.code == 403:
        current_app.logger.error(f"{get_user_or_ip()} - 403 '{request.method} {request.path}'")
        return render_template('error/403_forbidden.html'), 403

    elif error.code == 500:
        current_app.logger.error(
            f"{get_user_or_ip()} - {error.code} '{request.method} {request.path} {request.headers}'")

    else:
        current_app.logger.warning(f"{get_user_or_ip()} - {error.code} '{request.method} {request.path}'")

    return render_template("error/error_base.html", error_code=error.code, error_message=error.description), error.code
