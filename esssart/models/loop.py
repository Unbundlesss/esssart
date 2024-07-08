from collections import namedtuple
from .base import Base


class Loop(Base):
    table = "loop"
    fields = [
        "_id TEXT PRIMARY KEY",
        "barLength INTEGER",
        "user_name TEXT",
        "bps REAL",
        "instrument TEXT",
        "bufferPath TEXT",
        "bufferURL TEXT",
        "created INTEGER",
        "colourHistory BLOB",
        "cdn_attachment TEXT"
        "creatorUserName TEXT",
        "isBass INTEGER",
        "isDrum INTEGER",
        "isMic INTEGER",
        "isNote INTEGER",
        "length INTEGER",
        "length16ths INTEGER",
        "originalPitch INTEGER",
        "presetName TEXT",
        "primaryColour TEXT",
        "sampleRate INTEGER"
    ]

    index = ["loop_idx ON loop(_id, username)"]

    def __init__(self, db):
        super().__init__(db)
        self.Loop = namedtuple("Loop", self.field_names)
        self.tuple = self.Loop

    def create(self, **kwargs):
        self.add(kwargs)
