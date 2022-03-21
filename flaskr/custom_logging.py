import logging
from typing import List, Union

import requests

logging_config_prod = {
    'version': 1,
    'formatters': {
        'full': {
            'format': '{asctime} - {levelname:^8} - {name:^20} - {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'short': {
            'format': '{asctime} - {levelname:^8} - {name:^12} - {message}',
            'datefmt': '%H:%M:%S',
            'style': '{',
        },
        'discord': {
            'format': '{levelname:^8} - {name:^12} - {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://flask.logging.wsgi_errors_stream',

            'formatter': 'short',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'flaskr.log',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf8',

            'formatter': 'full',
            'level': 'NOTSET',
        },
        'discord': {
            'class': 'flaskr.custom_logging.DiscordHandler',
            "webhook_url": "https://discord.com/api/webhooks/955515354128461834/fPYM2kx0yK7u_CSdj5EcwG5e4NGp5_VtUr1UTkYBufQ_rMF5fTpiVVxPkBWSkRYb8DhI",
            'notify_users': ["351456719294955538"],

            'formatter': 'discord',
            'level': 'INFO',
        }},
    "loggers": {
        "flaskr": {
            "handlers": ["console", "file", "discord"],
            "level": "INFO",
        },
        "werkzeug": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    }
}

logging_config_dev = {
    'version': 1,
    'formatters': {
        'short': {
            'format': '{asctime} - {levelname:^8} - {name:^12} - {message}',
            'datefmt': '%H:%M:%S',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://flask.logging.wsgi_errors_stream',

            'formatter': 'short',
        }
    },

    "loggers": {
        "flaskr": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "werkzeug": {
            "handlers": ["console"],
            "level": "INFO",
        }
    }
}


class DiscordHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a Discord Server using webhooks.
    """

    def __init__(self, webhook_url: str, notify_users: List[Union[int, str]] = (), max_length: int = 2000):
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

            if record.levelno >= logging.ERROR and len(self._notify_users) > 0:
                self.write_to_discord(f"{users}")


        except Exception:
            self.handleError(record)
