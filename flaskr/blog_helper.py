from flaskr.db import get_db
from flask import abort, g


def get_post(post_id: int, check_author=True) -> dict:
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

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
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"] and not g.user["admin"]:
        abort(403)

    return post
