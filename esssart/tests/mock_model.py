from esssart.models.base import Base
from collections import namedtuple

class MockModel(Base):
    table = "mock_table"
    fields = [
        "id TEXT PRIMARY KEY",
        "name TEXT",
        "value INTEGER"
    ]

    def __init__(self, db):
        super().__init__(db)
        self.MockModel = namedtuple("MockModel", self.field_names)
        self.tuple = self.MockModel

