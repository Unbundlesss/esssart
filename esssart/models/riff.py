from collections import namedtuple
from . import Loop
from .base import Base


class SharedRiff(Base):
    extra = []
    table = 'shared_riff'
    fields = ["id TEXT PRIMARY KEY", "riff_name TEXT", "avatar TEXT", "creator TEXT", "contributors TEXT"]

    def __init__(self, db):
        super().__init__(db)
        self.SharedRiff = namedtuple("SharedRiff", self.field_names, )
        self.tuple = self.SharedRiff

    def add_loop(self, riff, loop):
        pass

    def get_loops(self, shared_riff_id):
        return self.db.shared_riff_loop.get_related_loops(shared_riff_id)

    def get_riff(self, shared_riff_id):
        return self.get_custom("id", shared_riff_id)
