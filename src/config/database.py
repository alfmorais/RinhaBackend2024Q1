import os

import sqlalchemy
from database import Database

metadata = sqlalchemy.MetaData()
DATABASE_URL = os.environ["DATABASE_URL"]


def get_db():
    database = Database(DATABASE_URL)

    try:
        yield database.connect()
    finally:
        database.disconnect()
