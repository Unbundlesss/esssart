import unittest
from unittest.mock import Mock, call
from ..models.base import Base

class TestBase(unittest.TestCase):
    def setUp(self):
        self.db = Mock()
        self.base = Base(self.db)

    def test_add(self):
        self.base.table = 'test_table'
        data = {'column1': 'value1', 'column2': 'value2'}
        self.base.add(data)

        self.db.cursor().execute.assert_called_once_with(
            "INSERT INTO test_table (column1, column2) VALUES (?, ?)",
            ('value1', 'value2')
        )
        self.db.commit.assert_called_once()