import mimetypes
from collections import namedtuple
from . import Loop
from .base import Base
import json
from esssart import app

class SharedRiff(Base):
    extra = []
    table = "shared_riff"
    fields = [
        "id TEXT PRIMARY KEY",
        "user_id TEXT",
        "action_timestamp INTEGER",
        "action_timestamp_iso TEXT",
        "app_version TEXT",
        "band TEXT",
        "bar_length INTEGER",
        "bps STRING",
        "brightness REAL",
        "color TEXT",
        "contributors TEXT",
        "created integer",
        "creator_id TEXT",
        "creators BLOB",
        "database_id TEXT",
        "image BOOLEAN",
        "image_attachment_id TEXT",
        "image_url TEXT",
        "layer_colors BLOB",
        "likes INTEGER",
        "magnitude STRING",
        "peak_data BLOB",
        "private BOOLEAN",
        "riff TEXT",
        "root INTEGER",
        "scale INTEGER",
        "sent_by TEXT",
        "title TEXT",
        "type TEXT",
        "user TEXT",
        'comment_count INTEGER',
        'comments TEXT'
    ]
    index = [
        "shared_riff_id_user_id ON shared_riff(id, user_id)",
        "shared_riff_creator_id ON shared_riff(creator_id)",
        "shared_riff_time ON shared_riff(action_timestamp)",
        "shared_riff_time_iso ON shared_riff(action_timestamp_iso)"
    ]

    def __init__(self, con):
        super().__init__(con)
        self.SharedRiff = namedtuple(
            "SharedRiff",
            self.field_names,
        )
        self.tuple = self.SharedRiff

    def add_loop(self, riff, loop):
        pass

    def get_loops(self, shared_riff_id):
        return self.app.shared_riff_loop.get_related_loops(shared_riff_id)

    def get_riff(self, shared_riff_id):
        return self.get_custom("id", shared_riff_id)

    def get_riff_dict(self, shared_riff_id):
        return self.get_custom("id", shared_riff_id, True)



