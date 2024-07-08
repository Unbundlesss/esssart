import unittest
from unittest.mock import Mock, call
from esssart.db import db, create_table_if_not_exists, snake_case


class TestDbFunctions(unittest.TestCase):
    def test_snake_case_converts_camel_case_to_snake_case(self):
        self.assertEqual(snake_case("CamelCase"), "camel_case")

    def test_snake_case_leaves_snake_case_unchanged(self):
        self.assertEqual(snake_case("snake_case"), "snake_case")

    def test_create_table_if_not_exists_does_not_create_table_when_exists(self):
        mock_model = Mock()
        mock_model.schema = "CREATE TABLE test_table (_id INTEGER PRIMARY KEY)"
        mock_model.table = "test_table"
        mock_model.db = Mock()
        mock_model.db.cur.fetchone.return_value = "test_table"

        create_table_if_not_exists(mock_model)

        mock_model.db.cur.execute.assert_called_once_with(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'"
        )
        mock_model.db.cur.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
