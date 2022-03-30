from typing import Iterator, List, Any


def count_users(string: str) -> int:
    """ Return the number of users in a string of comma-separated usernames. """
    if string == "" or string is None:
        return 0
    return len(string.split(","))


def parse_users(string: str) -> List[int]:
    """ Return the number of users in a string of comma-separated usernames. """
    if string == "" or string is None:
        return []
    return [int(u) for u in string.split(",")]


def user_set(string: str) -> "UserSet":
    """ Return a UserSet from a string of comma-separated user names. """
    return 0


class UserSet:
    """ Class to manage the list of users. """

    __slots__ = ["__users"]

    def __init__(self, text: str = None):
        if text is None or text == "":
            self.__users = set()
        else:
            try:
                self.__users = {int(u) for u in text.split(",")}
            except Exception:
                raise ValueError(f"Can't parse user list : {type(text)} {text}")

    def toggle(self, user_id: int):
        """ Toggle the user in the list. if it's in the list, remove it, else add it. """
        assert isinstance(user_id, int), f"user_id must be an int, not {user_id}"
        if user_id in self.__users:
            self.remove(user_id)
        else:
            self.add(user_id)

    def add(self, user_id: int):
        """ Add a user to the list. """
        assert isinstance(user_id, int), f"user_id must be an int, not {user_id}"
        self.__users.add(user_id)

    def remove(self, user_id: int):
        """ Remove a user from the list. """
        assert isinstance(user_id, int), f"user_id must be an int, not {user_id}"
        self.__users.remove(user_id)

    def join(self) -> str:
        """ Return the list as a string. """
        return ",".join(str(u) for u in self.__users)

    def is_empty(self) -> bool:
        """ Return True if the list is empty. """
        return len(self.__users) == 0

    def __len__(self) -> int:
        return len(self.__users)

    def __iter__(self) -> Iterator[int]:
        return iter(self.__users)

    def __repr__(self) -> str:
        return f"UserSet({self.__users})"
