import os
from logging.config import dictConfig

from flask import Flask
from werkzeug.exceptions import HTTPException


def create_app(testing: bool = False) -> Flask:
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)

    if testing:
        app.config.from_object('config.ConfigTest')
    elif app

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, blog, admin, user, search

    # register the blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(search.bp)

    # register sitemap blueprint
    from flaskr import sitemap
    app.register_blueprint(sitemap.bp)

    # register the error handlers
    from flaskr.error import error_handler
    app.register_error_handler(HTTPException, error_handler)

    app.add_url_rule("/", endpoint="index")

    return app
