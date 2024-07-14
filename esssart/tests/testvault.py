import unittest
from unittest.mock import Mock, MagicMock, call, patch
from esssart.db import db, create_table_if_not_exists, snake_case
from esssart.vault import Vault, File
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import os
from esssart.vault import Vault, File


class TestVault(unittest.TestCase):
    def setUp(self):
        # Setup temporary directory and initialize Vault with test data
        self.temp_dir = tempfile.mkdtemp()
        self.indata = {
            "json": os.path.join(self.temp_dir, "data/json"),
            "db": os.path.join(self.temp_dir, "data/db"),
            "avatar": os.path.join(self.temp_dir, "data/image/avatar"),
            "cover": os.path.join(self.temp_dir, "data/image/cover"),
            "banner": os.path.join(self.temp_dir, "data/image/banner"),
            "stem": os.path.join(self.temp_dir, "data/attachment/stem"),
            "temp": os.path.join(self.temp_dir, ".temp"),
        }
        self.vault = Vault(self.indata)

    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.temp_dir)

    def test_getattr_with_existing_item(self):
        # Test __getattr__ for an existing directory
        folder = self.vault.avatar
        self.assertEqual(folder.path, self.indata["avatar"])
        self.assertEqual(folder.type_key, "avatar")

    def test_getattr_with_non_existing_item(self):
        # Test __getattr__ for a non-existing directory, should raise AttributeError
        with self.assertRaises(AttributeError):
            _ = self.vault.non_existing_item

    @patch("esssart.vault.shutil.copy")
    @patch("esssart.vault.shutil.move")
    def test_folder_file_operations(self, mock_move, mock_copy):
        # Test file operations in a folder: save, import_file, export, export_with_name
        folder = self.vault.avatar
        test_file_content = b"Test content"
        test_file_name = "test.txt"
        source_file_name = "source.txt"
        imported_file_name = "imported.txt"
        export_folder = os.path.join(self.temp_dir, "export_dir")
        new_name = "new_name.txt"

        # Ensure export directory exists
        os.makedirs(export_folder, exist_ok=True)

        # Perform file operations
        folder.save(test_file_name, test_file_content)
        folder.import_file(source_file_name, imported_file_name)
        folder.export(test_file_name, export_folder)
        folder.export_with_name(test_file_name, export_folder, new_name)

        # Check if mock functions were called as expected
        mock_move.assert_called_once_with(
            source_file_name, os.path.join(folder.path, imported_file_name)
        )
        mock_copy.assert_has_calls(
            [
                call(
                    os.path.join(folder.path, test_file_name),
                    os.path.join(export_folder, test_file_name),
                ),
                call(
                    os.path.join(folder.path, test_file_name),
                    os.path.join(export_folder, new_name),
                ),
            ],
            any_order=True,
        )


if __name__ == "__main__":
    unittest.main()
