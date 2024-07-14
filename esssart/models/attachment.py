import mimetypes
from collections import namedtuple
from .base import Base
import json


class Attachment(Base):
    fields = [
        "id INTEGER PRIMARY KEY",
        "name TEXT UNIQUE",
        "key TEXT UNIQUE NOT NULL",
        "bucket TEXT",
        "type TEXT",
        "endpoint TEXT",
        "hash TEXT",
        "length INTEGER",
        "mime TEXT",
        "url TEXT",
        "local TEXT",
    ]
    extra = ["unique(key)"]
    index = ["attachment_key ON attachment(key)"]
    table = "attachment"

    def __init__(self, db):
        super().__init__(db)
        self.Attachment = namedtuple("Attachment", self.field_names)
        self.tuple = self.Attachment

    def pull_missing(self, limit=100):
        return self.get_many("local", "", limit)

    def get_attachment(self, _id):
        return self.get_one(_id)

    def add_attachment(self, att):
        self.add(att)

    def update_local(self, local, key):
        self.db.cur.execute(
            f"UPDATE {self.table} SET local = ? WHERE key = ?", (local, key)
        )
