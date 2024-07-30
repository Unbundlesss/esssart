import unittest
from unittest.mock import Mock
from mock_model import MockModel


class TestBaseWithMockModel(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.mock_db.cursor.return_value = self.mock_db.cur
        self.mock_model = MockModel(self.mock_db)

    def test_get_custom(self):
        self.mock_db.cur.fetchone.return_value = ("some_id", "test_name", 123)
        result = self.mock_model.get_custom("id", "some_id")
        self.assertEqual(result, ("some_id", "test_name", 123))

    def test_add(self):
        self.mock_model.add(id="some_id", name="test_name", value=123)
        self.mock_db.cursor().execute.assert_called_with(
            "INSERT INTO mock_table (id, name, value) VALUES (?, ?, ?)",
            ("some_id", "test_name", 123),
        )

    def test_colcheck_valid(self):
        try:
            self.mock_model.colcheck("id")
        except ValueError:
            self.fail("colcheck() raised ValueError unexpectedly!")

    def test_colcheck_invalid(self):
        with self.assertRaises(ValueError):
            self.mock_model.colcheck("invalid_column")

    def test_update(self):
        self.mock_model.update(id="some_id", name="updated_name", value=456)
        self.mock_db.cursor().execute.assert_called_with(
            "UPDATE mock_table SET name = ?, value = ? WHERE id = ?",
            ("updated_name", 456, "some_id"),
        )

    def test_delete(self):
        self.mock_model.delete(id="some_id")
        self.mock_db.cursor().execute.assert_called_with(
            "DELETE FROM mock_table WHERE id = ?", ("some_id",)
        )

    def test_get_all(self):
        self.mock_db.cur.fetchall.return_value = [
            ("some_id", "test_name", 123),
            ("another_id", "another_name", 456),
        ]
        result = self.mock_model.get_all()
        self.assertEqual(
            result, [("some_id", "test_name", 123), ("another_id", "another_name", 456)]
        )


if __name__ == "__main__":
    unittest.main()

