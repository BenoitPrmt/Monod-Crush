from flask import render_template, current_app, request, redirect
from werkzeug.exceptions import HTTPException


def error_handler(error: HTTPException):
    """ Error handler for HTTP exceptions. """

    if error.code == 500:
        current_app.logger.error(f"{request.remote_addr} - {error.code}"
                                 f" '{request.method} {request.url} {request.headers}'")

    # redirect foo/bar/something/  to foo/bar/something
    # check if not end with foo/bar////////// for not enter in loop
    elif error.code == 404 and request.path.endswith('/') and not request.path.endswith('//'):
        return redirect(request.path[:-1])

    else:
        current_app.logger.warning(
            f"{request.headers.get('X-Real-IP', request.remote_addr)} - {error.code} '{request.method} {request.url}'")

    return render_template("error/error_base.html", error_code=error.code, error_message=error.description), error.code
