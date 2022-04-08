from __future__ import annotations

import re
from datetime import date
from typing import Tuple, Literal, Union, Optional, List, Dict, Any

from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import get_db


class User:
    """ User class """

    id: int
    username: str
    accreditation: Literal[0, 1, 2, 3]  # 0 = banned, 1 = user, 2 = moderator, 3 = admin

    @classmethod
    def get_user_by_id(cls, user_id) -> Optional[User]:
        """ Get user by id """
        r = get_db().execute("SELECT id, username, accreditation FROM user WHERE id = ?", (user_id,)).fetchone()

        if not r:
            raise ValueError(f"User {user_id} not found")

        user = User()
        user.id = r["id"]
        user.username = r["username"]
        user.accreditation = r["accreditation"]

        return user

    @classmethod
    def get_user_by_name(cls, username) -> Optional[User]:
        """ Get user by id """
        r = get_db().execute("SELECT id, username, accreditation FROM user WHERE username = ?", (username,)).fetchone()

        if not r:
            raise ValueError(f"User {username} not found")

        user = User()
        user.id = r["id"]
        user.username = r["username"]
        user.accreditation = r["accreditation"]

        return user

    @classmethod
    def get_user_by_name_or_404(cls, username: str) -> User:
        """ Get user by id or return 404 """

        try:
            user = User.get_user_by_name(username)
        except ValueError as e:
            abort(404, e)  # TODO raise 404 error redirecting to 404_user_not_found.html
        else:
            return user

    @classmethod
    def get_all_username(cls, staff_only=False) -> List[str]:
        """ Get all usernames """
        if staff_only:
            return [r["username"] for r in
                    get_db().execute("SELECT username FROM user WHERE accreditation > 1").fetchall()]
        else:
            return [r["username"] for r in get_db().execute("SELECT username FROM user").fetchall()]

    @classmethod
    def create(cls, username: str, date_of_birth: Union[date, str], password: str) -> User:
        """ Create a new user """

        # check if username is valid
        is_valid, msg = check_username(username)
        if not is_valid:
            raise ValueError(msg)

        # check if password is valid
        is_valid, msg = check_password_strength(password)
        if not is_valid:
            raise ValueError(msg)

        # check if date of birth is valid
        if isinstance(date_of_birth, str):
            try:
                date_of_birth = date.fromisoformat(date_of_birth)
            except ValueError:
                raise ValueError("Invalid date of birth")

        is_valid, msg = check_date_of_birth(date_of_birth)
        if not is_valid:
            raise ValueError(msg)

        db = get_db()
        r = db.execute(
            "INSERT INTO user (username, date_of_birth, password) VALUES (?, ?, ?)",
            (username, date_of_birth, generate_password_hash(password)),
        )
        db.commit()

        user = User()
        user.id = r.lastrowid
        user.username = username
        user.accreditation = 1

        return user

    @classmethod
    def login(cls, username: str, password: str) -> User:
        """ Login user """

        db = get_db()
        r = db.execute("SELECT id, username, password, accreditation FROM user WHERE username = ?",
                       (username,)).fetchone()

        if not r:
            raise ValueError("Nom d'utilisateur ou mot de passe incorrect")

        if not check_password_hash(r["password"], password):
            raise ValueError("Nom d'utilisateur ou mot de passe incorrect")

        if r["accreditation"] == 0:
            raise ValueError("Votre compte a été banni")

        user = User()
        user.id = r["id"]
        user.username = r["username"]
        user.accreditation = r["accreditation"]

        return user

    # def new_post(self, message: str, is_anonyme: bool = True) -> None:
    #     """ Create a new post """
    #
    #     Post.create(self.id, message, is_anonyme)
    #
    # def comment(self, post_id: int, message: str, is_anonyme: bool) -> None:
    #     """ Comment on a post """
    #
    #     Comment.create(self.id, post_id, message, is_anonyme)
    #
    # def like(self, post_id: int) -> None:
    #     """ Like a post """
    #
    #     Post.get_post_or_404(post_id).like(self.id)
    #
    # def unlike(self, post_id: int) -> None:
    #     """ Unlike a post """
    #
    #     Post.get_post_or_404(post_id).unlike(self.id)
    #
    # def report(self, post_id: int) -> None:
    #     """ Report a post if exist and if not already reported  """
    #
    #     Post.get_post_or_404(post_id).report(self.id)

    def get_full_info(self) -> Dict[str, Any]:
        """ Get all user info """

        infos = get_db().execute("SELECT * FROM user WHERE id = ?", (self.id,))

        return dict(infos.fetchone())

    def promote(self, level: Literal[1, 2, 3]) -> None:
        """ Promote user """
        db = get_db()
        db.execute("UPDATE user SET accreditation = ? WHERE id = ?", (level, self.id))
        db.commit()
        self.accreditation = level

    def __repr__(self) -> str:
        """ Representation of user """
        return f"<User {self.username} {self.id}>"


def check_password_strength(password: str) -> Tuple[bool, str]:
    """ Check if the password is strong enough """
    if len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères"
    elif len(password) > 25:
        return False, "Le mot de passe doit contenir 25 caractères maximum"

    return True, ""


def check_username(username: str) -> Tuple[bool, str]:
    """ Check if the username is available """
    if len(username) < 3:
        return False, "Votre nom d'utilisateur doit contenir au moins 3 caractères"
    elif len(username) > 20:
        return False, "Votre nom d'utilisateur doit contenir 20 caractères maximum"
    elif not re.match(r'^[A-Za-z][A-Za-z0-9_-]+$', username):
        return False, "Votre nom d'utilisateur doit commencer par une lettre et peut contenir uniquement des lettres," \
                      " nombres, tirets du bas et tirets"

    db = get_db()
    if db.execute("SELECT 1 FROM user WHERE username = ?", (username,)).fetchone() is not None:
        return False, "Ce nom d'utilisateur est déjà pris"

    return True, ""


def check_date_of_birth(date_of_birth: date) -> Tuple[bool, str]:
    """ Check if the date of birth is valid """

    if date_of_birth > date.today():
        return False, "Vous voyagez dans le temps ? Votre date de naissance doit être dans le passé"
    elif date_of_birth < date(year=1920, month=1, day=1):
        return False, "Veuillez indiquer une date de naissance valide"

    return True, ""
