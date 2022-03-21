from flask import render_template, app, current_app, request
from werkzeug.exceptions import HTTPException


def error_handler(error: HTTPException):
    """ Error handler for HTTP exceptions. """

    current_app.logger.warning(f"Error {error.code}: {request.url} by {request.remote_addr}")

    return render_template("error/all_error.html", error_code=error.code), error.code
