import os
import sqlite3
from typing import Dict, Any, NamedTuple
from collections import namedtuple
from sqlite3 import Connection, Cursor
from .models import Base
from .models import SharedRiff, Loop, User, JoinRiffLoop, Attachment
import re
from .vault import Vault

dbpath = "data/db/esssart.database.2.db"
os.makedirs(os.path.dirname(dbpath), exist_ok=True)
is_new = True if not os.path.exists(dbpath) else False
con = sqlite3.connect(dbpath)
con.execute("PRAGMA foreign_keys = ON")
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


# stick the whole thing into the app wad
class DbConnect(NamedTuple):
    user: User
    shared_riff: SharedRiff
    loop: Loop
    attachment: Attachment
    join_riff_loop: JoinRiffLoop
    vault: Vault
    con: Connection
    cur: Cursor

    def get(self, name):
        return self.__dict__[name]

    def init_all(self):
        self.shared_riff.init()
        self.loop.init()
        self.attachment.init()
        self.join_riff_loop.init()
        self.user.init()


model_instances = {snake_case(cls.__name__): cls(con) for cls in model_classes}
other_instances = {"vault": Vault(indata), "con": con, "cur": con.cursor()}

# Combine the dictionaries
instances = {**model_instances, **other_instances}

# stick the whole thing into the app wad
app = DbConnect(*instances.values())

# make app available to models
Base.set_app(app)


# idempotent
def create_table_if_not_exists(model):
    """
    Create a table in the database if it does not already exist.

    Args:
        model (base): The model representing the table.

    Returns:
        None
    """
    table_name = model.table
    app.cur.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    if not app.cur.fetchone():
        model.init()


# idempotent


# create_table_if_not_exists(Loop.schema, "loop")
# create_table_if_not_exists(SharedRiff.schema, "shared_riff")
# create_table_if_not_exists(SharedRiff.m2m_schema, "shared_riff_loop")
