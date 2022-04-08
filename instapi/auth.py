import os
from pathlib import Path

from instagrapi import Client

from settings import INSTA_USERNAME, INSTA_PASSWORD


def login() -> Client:
    cl = Client()
    if not os.path.exists("tmp/cookies.json"):
        # create a new file and directory
        os.makedirs("tmp", exist_ok=True)
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)
        cl.dump_settings(Path('tmp/dump.json'))
    else:
        cl.load_settings(Path("tmp/cookies.json"))
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)
        cl.get_timeline_feed()  # check session
    return cl
