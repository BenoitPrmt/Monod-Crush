from flask import render_template
from werkzeug.exceptions import HTTPException

def error_handler(error: HTTPException):
    """ Error handler for HTTP exceptions. """
    return render_template("error/all_error.html", error_code=error.code), error.code
