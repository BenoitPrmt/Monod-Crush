import logging
import os
from typing import List, Union

import requests
from flask import Flask
from werkzeug.exceptions import HTTPException
from flaskr import auth_helper
from flaskr.error import error_handler

from flask.logging import default_handler


#


def create_app(test_config: dict = None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if not app.debug and not app.testing:
        # setup logging DiscordHandler with discord webhook
        webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
        if webhook_url:
            webhook_url = "https://discord.com/api/webhooks/954368771110359121/mS5dYS9CL2IGLMiWtZis2abb036YrSHWtNZ269xEZHyZSKzK19ss8zz0MWzKMNizvwYc"
            discordHandler = DiscordHandler(webhook_url)

            discordHandler.setLevel(logging.INFO)
            app.logger.addHandler(discordHandler)
            discordHandler.setFormatter(logging.Formatter("%(message)s"))

        logging.getLogger('werkzeug').removeHandler(default_handler)

        # setup logging fileHandler
        file_handler = logging.FileHandler("flaskr.log")
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register.py the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, blog, admin, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(auth_helper.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)

    # register the error handlers
    app.register_error_handler(HTTPException, error_handler)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app


class DiscordHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a Discord Server using webhooks.
    """

    def __init__(self, webhook_url: str, notify_users: List[Union[int, str]] = None, max_length: int = 2000):
        logging.Handler.__init__(self)

        if not webhook_url:
            raise ValueError("webhook_url parameter must be given and can not be empty!")

        if notify_users is None:
            notify_users = []

        self._notify_users = notify_users
        self._url = webhook_url
        self._max_length = max_length

    def write_to_discord(self, message: str):
        request = requests.post(self._url, data={"content": message})

        if not request.ok:
            if request.status_code == 404:
                raise requests.exceptions.InvalidURL(
                    f"Discord WebHook URL returned status 404, is the URL correct?\nResponse = {request.text}")

            else:
                raise requests.exceptions.HTTPError(
                    f"Discord WebHook returned status code {request.status_code}, Message = {request.text}"
                )

    def emit(self, record: logging.LogRecord) -> None:
        """ Emit a record. """
        try:
            msg = self.format(record)

            trimmed_msg = [msg[i:i + self._max_length] for i in range(0, len(msg), self._max_length)]
            users = '\n'.join(f'<@{user}>' for user in self._notify_users)

            for msg in trimmed_msg:
                self.write_to_discord(f"```{msg}```")

            if record.levelno >= logging.ERROR:
                self.write_to_discord(f"```{users}```")


        except Exception:
            self.handleError(record)
