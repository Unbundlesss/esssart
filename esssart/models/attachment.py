from collections import namedtuple
from .base import Base
import json


class Attachment(Base):
    fields = ["_id INTEGER PRIMARY KEY", "key TEXT UNIQUE NOT NULL", "type TEXT", "endpoint TEXT", "hash TEXT",
              "length INTEGER", "mime TEXT", "url TEXT", "local TEXT"]
    extra = ["unique(key)"]
    table = "attachment"

    def __init__(self, db):
        super().__init__(db)
        self.Attachment = namedtuple("Attachment", self.field_names)
        self.tuple = self.Attachment

    def create(self, dict):
        self.add(dict)

    def pull_missing(self, qtype, limit=100):
        return self.get_many('type', qtype, limit)

        # "endpoint": "ndls-att2.ams3.digitaloceanspaces.com",
        # "hash": "",
        # "key": "attachments/oggAudio/band2e9c40ccec/1181db40c5ef11ea9b40c0dd3fc95868",
        # "length": 296977,
        # "mime": "audio/ogg",
        # "url": "https://ndls-att2.ams3.digitaloceanspaces.com/attachments/oggAudio/band2e9c40ccec/1181db40c5ef11ea9b40c0dd3fc95868"
