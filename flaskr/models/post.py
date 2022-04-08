from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Tuple, Union

import requests
from flask import current_app, abort, g

from flaskr.db import get_db


class Post:
    """ Post class """

    id: int
    message: str
    user_id: int
    user_username: str
    is_anonymous: bool
    created_at: datetime
    edited: bool
    edited_at: Optional[datetime]

    reported_by: Optional[Tuple[int]]
    liked_by: Optional[Tuple[int]]

    @classmethod
    def get_post_or_404(cls, post_id: int, check_user_is_owner=True) -> Post:
        """ Get post by id or return 404 """

        try:
            post = cls.get_post(post_id)
        except ValueError:
            abort(404, f"Post id {post_id} doesn't exist")
        else:
            if check_user_is_owner and g.user is not None and post.user_id != g.user.id:
                abort(403)
            return post

    @classmethod
    def get_post(cls, post_id: int) -> Post:
        """ Get post by id """

        db = get_db()
        row = db.execute("""
               SELECT * ,
               (SELECT user_id FROM like WHERE post_id = p.id ) as liked_by,
               (SELECT user_id FROM report WHERE post_id = p.id ) as reported_by
               FROM post p
               JOIN user u ON p.user_id = u.id
               WHERE p.id = ?""", (post_id,)).fetchone()

        if row is None:
            raise ValueError("Post doesn't exist")

        post = Post()
        for key in row.keys():
            if key == "reported_by":
                setattr(post, key, parse_user_list(row[key]))
            elif key == "liked_by":
                setattr(post, key, parse_user_list(row[key]))
            else:
                setattr(post, key, row[key])
        return post

    @classmethod
    def get_posts(cls) -> List[Post]:
        """ Get posts """

        db = get_db()
        rows = db.execute("""
                       SELECT p.id, p.message,p.is_anonymous, p.user_id, p.created_at, p.edited, u.username,
                       (SELECT GROUP_CONCAT(user_id) FROM like WHERE post_id = p.id ) as liked_by,
                       (SELECT GROUP_CONCAT(user_id) FROM report WHERE post_id = p.id ) as reported_by
                       FROM post p
                       JOIN user u ON p.user_id = u.id
                       WHERE p.status = 'visible'
                       ORDER BY p.created_at DESC""").fetchall()

        posts = []
        for row in rows:
            post = Post()
            for key in row.keys():
                current_app.logger.info(f"{key} : {row[key]}")
                if key == "reported_by":
                    setattr(post, key, parse_user_list(row[key]))
                elif key == "liked_by":
                    setattr(post, key, parse_user_list(row[key]))
                else:
                    setattr(post, key, row[key])
            posts.append(post)

        return posts

    @classmethod
    def get_posts_for_moderation(cls) -> List[Post]:
        """ Get posts """

        db = get_db()
        rows = db.execute("""
                           SELECT p.id, p.message,p.is_anonymous, p.user_id, p.created_at, p.edited, u.username,
                           (SELECT GROUP_CONCAT(user_id) FROM like WHERE post_id = p.id ) as liked_by,
                           (SELECT GROUP_CONCAT(user_id) FROM report WHERE post_id = p.id ) as reported_by
                           FROM post p
                           JOIN user u ON p.user_id = u.id
                           WHERE reported_by NOT NULL
                           ORDER BY p.created_at DESC""").fetchall() # TODO: trier par nombre report

        posts = []
        for row in rows:
            post = Post()
            for key in row.keys():
                current_app.logger.info(f"{key} : {row[key]}")
                if key == "reported_by":
                    setattr(post, key, parse_user_list(row[key]))
                elif key == "liked_by":
                    setattr(post, key, parse_user_list(row[key]))
                else:
                    setattr(post, key, row[key])
            posts.append(post)

        return posts

    @classmethod
    def get_posts_by_user(cls, user_id: int) -> List[Post]:
        """ Get posts by user """

        db = get_db()
        r = db.execute("""
                       SELECT * ,
                       (SELECT user_id FROM like WHERE post_id = p.id ) as liked_by,
                       (SELECT user_id FROM report WHERE post_id = p.id ) as reported_by
                       FROM post p
                       JOIN user u ON p.user_id = u.id
                       WHERE u.id = ? AND p.status = 'visible'
                       ORDER BY p.created_at DESC""", (user_id,)).fetchall()

        posts = []
        for row in r:
            post = Post()
            for key in row.keys():
                if key == "reported_by":
                    setattr(post, key, parse_user_list(row[key]))
                elif key == "liked_by":
                    setattr(post, key, parse_user_list(row[key]))
                else:
                    setattr(post, key, row[key])
            posts.append(post)

        return posts

    @classmethod
    def create(cls, message: str, author_id: int, is_anonymous: bool = True):
        """ Create post """

        is_valid, msg = check_message_body(message)
        if not is_valid:
            raise ValueError(msg)

        message = auto_moderate_text(message)

        db = get_db()
        r = db.execute("""INSERT INTO post (message, is_anonymous, user_id)
                     VALUES (?, ?, ?)""", (message, is_anonymous, author_id))
        db.commit()

        return cls.get_post(r.lastrowid)

    def update(self, message: str, reset_report: bool = True):
        """ Update post """

        is_valid, msg = check_message_body(message)
        if not is_valid:
            raise ValueError(msg)

        message = auto_moderate_text(message)

        db = get_db()
        db.execute("""UPDATE post SET message = ? WHERE id = ?""",
                   (message, self.id))

        if reset_report:
            db.execute("""DELETE FROM report WHERE post_id = ?""", (self.id,))
            db.execute("""UPDATE post SET status = 'visible' WHERE id = ?""", (self.id,))
        db.commit()

    def like(self, user_id: int):
        """ Like post """

        db = get_db()
        db.execute("""INSERT INTO like (post_id, user_id) VALUES (?, ?)""", (self.id, user_id))
        db.commit()

    def unlike(self, user_id: int):
        """ Unlike post """

        db = get_db()
        db.execute("""DELETE FROM like WHERE post_id = ? AND user_id = ?""", (self.id, user_id))
        db.commit()

    def report(self, user_id: int):
        """ Report post """
        db = get_db()

        if len(self.reports) == 2:
            db.execute("""UPDATE post SET status = 'hidden' WHERE id = ?""", (self.id,))

        db.execute("""INSERT INTO report (post_id, user_id) VALUES (?, ?)""", (self.id, user_id))
        db.commit()

    def clear_report(self) -> None:
        """ Unreport post """

        db = get_db()
        db.execute("""DELETE FROM report WHERE post_id = ?""", (self.id,))
        db.commit()

    def hide(self) -> None:
        """ Hide post """

        db = get_db()
        db.execute("""UPDATE post SET status = 'hidden' WHERE id = ?""", (self.id,))
        db.commit()

    def show(self) -> None:
        """ change status to 'visible' """

        db = get_db()
        db.execute("""UPDATE post SET status = 'visible' WHERE id = ?""", (self.id,))
        db.commit()

    def delete(self) -> None:
        """ Delete post """

        db = get_db()
        db.execute("""DELETE FROM post WHERE id = ?""", (self.id,))
        db.commit()


def parse_user_list(user_list: Union[str, None, int]) -> List[int]:
    """ Parse user list """

    if user_list:
        if isinstance(user_list, int):
            return [user_list]
        return [int(user_id) for user_id in user_list.split(",")]
    return []


def check_message_body(text: str) -> Tuple[bool, str]:
    """ Check if the message body is empty and have less than 300 characters."""
    if not 1 <= len(text):
        return False, "Le message ne peut pas être vide."
    if not len(text) <= 300:
        return False, "Le message ne peut pas dépasser 300 caractères. Soyez plus concis."

    return True, ""


def auto_moderate_text(text: str) -> str:
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
        'api_user': '856965332',  # TODO : change this
        'api_secret': '3xBURpFF2fznLme5ceVw'
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
