import os
import sqlite3
from typing import Dict, Any, NamedTuple
from collections import namedtuple
from sqlite3 import Connection, Cursor
from .models import Base
from .models import SharedRiff, Loop, User, JoinRiffLoop, Attachment
import re
from .vault import Vault
from .config import make_config

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

    def create_table_if_not_exists(self, model):
        table_name = model.table
        self.cur.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )
        if not self.cur.fetchone():
            model.init()

def snake_case(name):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", name).lower()


def make_app(config=None):
    config = config if config is not None else make_config()
    [dbpath, datapaths] = config
    is_new = True if not os.path.exists(dbpath) else False

    # creates directories
    vault = Vault(datapaths)

    con = sqlite3.connect(dbpath)
    con.execute("PRAGMA foreign_keys = ON")

    # initialize models and join non-models
    model_classes = [User, SharedRiff, Loop, Attachment, JoinRiffLoop]
    model_instances = {snake_case(cls.__name__): cls(con) for cls in model_classes}
    other_instances = {"vault": vault, "con": con, "cur": con.cursor()}

    # Combine the dictionaries
    instances = {**model_instances, **other_instances}

    # stick the whole thing into the app wad
    app = DbConnect(*instances.values())

    # make app available to models
    Base.set_app(app)

    return app



# make idempotent
# create_table_if_not_exists(Loop.schema, "loop")
# create_table_if_not_exists(SharedRiff.schema, "shared_riff")
# create_table_if_not_exists(SharedRiff.m2m_schema, "shared_riff_loop")
