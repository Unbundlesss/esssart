import os
import sqlite3
from collections import namedtuple
from typing import Dict, Any
from typing import Union
from sqlite3 import Connection, Cursor
from unittest.mock import Mock

from .models import Base
from .models import SharedRiff, Loop, User, JoinRiffLoop, Attachment
import re
from .vault import Vault

dbpath = "data/db/esssart.database.db"
is_new = True if not os.path.exists(dbpath) else False

pattern = re.compile(r"(?<!^)(?=[A-Z])")

indata = {
    "json": "data/json",
    "db": "data/db",
    "avatar": "data/image/avatar",
    "cover": "data/image/cover",
    "banner": "data/image/banner",
    "stem": "data/attachment/stem",
    "temp": ".temp",
}

con = sqlite3.connect(dbpath)


def snake_case(name):
    """
    Convert a string to snake case.

    Args:
        name (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return pattern.sub("_", name).lower()


# initialize models and join non-models
model_classes = [User, SharedRiff, Loop, Attachment, JoinRiffLoop]


# This block of code is responsible for creating instances of the models and other necessary components
# and storing them in a dictionary for easy access.
# A dictionary named 'instances' is created with the keys being the snake_case version of the class names
# and the values being instances of those classes. The connection object 'con' is passed to each class
# during instantiation.
instances: Dict[str, Union[Base, Vault, Connection, Cursor, Attachment]] = {
    **{snake_case(cls.__name__): cls(con) for cls in model_classes},
    **{k: v for k, v in zip(["vault", "con", "cur"], [Vault(indata), con, con.cursor()])},
}

# stick the whole thing into the db wad
db: namedtuple = namedtuple("dbconnection", instances.keys())(**instances)


# idempotent
def create_table_if_not_exists(model: Base):
    """
    Create a table in the database if it does not already exist.

    Args:
        model (object): The model representing the table.

    Returns:
        None
    """
    schema, table_name = model.schema, model.table
    model.db = Mock()
    model.db.cur.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    if not model.db.cur.fetchone():
        model.db.cur.execute(schema)
        model.db.cur.commit()


# idempotent


# create_table_if_not_exists(Loop.schema, "loop")
# create_table_if_not_exists(SharedRiff.schema, "shared_riff")
# create_table_if_not_exists(SharedRiff.m2m_schema, "shared_riff_loop")
