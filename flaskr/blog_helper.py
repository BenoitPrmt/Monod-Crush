from typing import Tuple

from flask import abort, current_app, g

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


def moderate_message_body(text) -> str:
    data = {
        'text': text,
        'mode': 'standard',
        'lang': 'fr',
        'opt_countries': 'us,gb,fr',
        'api_user': '856965332',
        'api_secret': '3xBURpFF2fznLme5ceVw'
    }

    # {'status': 'success', 'request': {'id': 'req_bzWZ6JQImX740V0PX2XAj', 'timestamp': 1648817142.015168, 'operations': 1}, 'profanity': {'matches': []}, 'personal': {'matches': []}, 'link': {'matches': []}}

    r = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)

    output = json.loads(r.text)

    current_app.logger.info(output)

    for i in output["profanity"]["matches"]:
        current_app.logger.info(i)
        text = text.replace(i["match"][1:], "*" * len(i["match"][1:]))

    return text


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
