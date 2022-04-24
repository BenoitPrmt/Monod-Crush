"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = "dev"


class ProdConfig(Config):
    """Production config."""
    # generate a secret key with : `python -c 'import secrets; print(secrets.token_hex())'`
    SECRET_KEY = "dev"

    DISCORD_WEBHOOK_URL: str = "https://discord.com/api/webhooks/955515354128461834/" \
                               "fPYM2kx0yK7u_CSdj5EcwG5e4NGp5_VtUr1UTkYBufQ_rMF5fTpiVVxPkBWSkRYb8DhI"

    DISCORD_NOTIFY_USERS: list = ["351456719294955538"]

    SITE_ENGINE_API_USER: str = "856965332"
    SITE_ENGINE_API_SECRET: str = "3xBURpFF2fznLme5ceVw"


class DevConfig(Config):
    """Development config."""


class TestingConfig(Config):
    """Testing config."""
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'test'

    DISCORD_WEBHOOK_URL: str = ""
    DISCORD_NOTIFY_USERS: list = []

    SITE_ENGINE_API_USER: str = ""
    SITE_ENGINE_API_SECRET: str = ""
