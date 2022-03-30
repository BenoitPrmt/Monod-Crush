import os
from logging.config import dictConfig

from flask import Flask
from werkzeug.exceptions import HTTPException

from flaskr.custom_logging import logging_config_dev, logging_config_prod


def create_app(test_config: dict = None) -> Flask:
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",  # TODO change this
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # setup logging
    if app.debug or app.testing:
        dictConfig(logging_config_dev)
    else:
        dictConfig(logging_config_prod)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # add custom function to the database
    db.register_custom_functions()

    # apply the blueprints to the app
    from flaskr import auth, blog, admin, user, auth_helper, search

    # register the blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(auth_helper.bp)
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

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
