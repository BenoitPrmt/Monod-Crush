from typing import Tuple

from flask import abort, current_app, g
from settings import SITE_ENGINE_API_USER, SITE_ENGINE_API_SECRET

from flaskr.db import get_db
import requests
import json


def check_message_body(text: str) -> Tuple[bool, str]:
    """ Check if the message body is empty and have less than 300 characters."""
    if not 1 <= len(text):
        return False, "Le message ne peut pas être vide."
    if not len(text) <= 300:
        return False, "Le message ne peut pas dépasser 300 caractères. Soyez plus concis."

    return True, ""


def moderate_message_body(text: str) -> str:
    """ CHeck with the API if the message is clean or not.
    If it is not clean, we replace the word with asterisks.
    example : "Hello world" -> "H**** w***" """

    if current_app.testing or current_app.debug:
        return text

    data = {
        'text': text,
        'mode': 'standard',
        'lang': 'fr',
        'opt_countries': 'us,gb,fr',
        'api_user': SITE_ENGINE_API_USER,
        'api_secret': SITE_ENGINE_API_SECRET
    }

    rep = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data).json()

    if len(rep["profanity"]["matches"]) > 0:
        current_app.logger.error("Message contains profanity")

    text = list(text)
    for match in rep["profanity"]["matches"]:

        for c in range(match["start"], match["end"] + 1):
            if text[c].isalnum() and c != 0 and text[c - 1] != " ":
                text[c] = "*"

    return "".join(text)


def get_post(post_id: int, check_author=True) -> dict:
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    need to be after @login_required

    :param post_id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = get_db().execute(
        """SELECT p.id, p.body, p.created, p.author_id, u.username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.id = ?""", (post_id,)).fetchone()

    if post is None:
        abort(404, f"Le post {post_id} n'existe pas.")

    if check_author and post["author_id"] != g.user["id"] and not g.user["admin"]:
        abort(403)

    return post
