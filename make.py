import sqlite3
import argparse

import logging

LOG_FORMAT = "{levelname:^8} - {message}"


logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, style="{")
log = logging.getLogger(__name__)

con = sqlite3.connect('example.db')
cur = con.cursor()


def populate_db(quantity: int = 10) -> None:
    log.info("populate")

    from faker import Faker
    fake = Faker()

    # cur.execute("INSERT INTO UserData VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # cur.execute("INSERT INTO UserData VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    sql = """INSERT INTO UserData (firstName,lastName, dateOfBirth, inSearchFo)
    VALUES(?,?,?)"""

    
    cur.execute(sql, (fake.name(), fake.name(), 1))
    cur.execute(sql, (fake.name(), fake.name(), '2006-01-05', 1))


def clean_db() -> None:
    log.info("clean")


def create_db() -> None:
    log.info("setup")
    # cur.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')
    cur.execute("""CREATE TABLE IF NOT EXISTS UserData (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"firstName"	TEXT NOT NULL,
	"lastName"	TEXT NOT NULL,
	"dateOfBirth"	TEXT NOT NULL,
	"inSearchFor"	INTEGER NOT NULL,
	"class"	INTEGER,
	"speciality"	INTEGER
    );""")


actions = {"init": create_db, "clean": clean_db, "populate": populate_db}

parser = argparse.ArgumentParser()
parser.add_argument("action", type=str,
                    help="action a executé", choices=actions.keys())

args = parser.parse_args()
log.debug(args)
actions[args.action]()

con.commit()
con.close()
