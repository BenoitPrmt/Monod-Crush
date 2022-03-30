from typing import Tuple

from flask import abort, g

from flaskr.db import get_db


def check_message_body(text: str) -> Tuple[bool, str]:
    """ Check if the message body is empty and have less than 300 characters."""
    if not 1 <= len(text):
        return False, "Le message ne peut pas être vide."
    if not len(text) <= 300:
        return False, "Le message ne peut pas dépasser 300 caractères. Soyez plus concis."

    return True, ""


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
        abort(401)

    return post
