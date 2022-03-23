from flask import render_template, app, current_app, request
from werkzeug.exceptions import HTTPException


def error_handler(error: HTTPException):
    """ Error handler for HTTP exceptions. """

    current_app.logger.warning(f"{request.remote_addr} {error.code} '{request.method} {request.url}' {request.data}")

    return render_template("error/all_error.html", error_code=error.code), error.code
