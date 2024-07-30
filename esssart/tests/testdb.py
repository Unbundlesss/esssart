import unittest
from unittest.mock import Mock, call
from esssart.app import create_table_if_not_exists, snake_case, DbConnect
from esssart.models.base import Base

class TestDbConnect(unittest.TestCase):
    def setUp(self):
        self.mock_con = Mock()
        self.mock_cur = Mock()
        self.mock_con.cur = self.mock_cur
        self.mock_model = Mock(spec=Base)
        self.mock_model.table = "mock_table"
        self.mock_model.schema = "CREATE TABLE mock_table (id TEXT PRIMARY KEY)"
        self.mock_model.db = self.mock_con


    def test_snake_case(self):
        self.assertEqual(snake_case("TestString"), "test_string")
        self.assertEqual(snake_case("anotherTestString"), "another_test_string")
        self.assertEqual(snake_case("YetAnotherTest"), "yet_another_test")

if __name__ == "__main__":
    unittest.main()