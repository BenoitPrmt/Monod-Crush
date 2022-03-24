from flask import render_template, current_app, request
from werkzeug.exceptions import HTTPException


def error_handler(error: HTTPException):
    """ Error handler for HTTP exceptions. """

    if error.code == 500:
        current_app.logger.error(f"{request.remote_addr} {error.code}"
                                 f" '{request.method} {request.url} {request.headers}'")

    else:
        current_app.logger.warning(f"{request.remote_addr} {error.code} '{request.method} {request.url}'")

    return render_template("error/all_error.html", error_code=error.code), error.code
