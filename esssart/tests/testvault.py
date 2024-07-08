import unittest
from unittest.mock import Mock, MagicMock, call, patch
from esssart.db import db, create_table_if_not_exists, snake_case
from esssart.vault import Vault, File

class TestVault(unittest.TestCase):
    # @patch('os.makedirs')
    def setUp(self):
        self.indata = {
            "json": "data/json",
            "db": "data/db",
            "avatar": "data/image/avatar",
            "cover": "data/image/cover",
            "banner": "data/image/banner",
            "stem": "data/attachment/stem",
            "temp": ".temp",
        }
        self.vault = Vault(self.indata)


    def test_getattr_with_existing_item(self):
        folder = self.vault.avatar
        self.assertEqual(folder.path, 'data/image/avatar')
        self.assertEqual(folder.type_key, 'avatar')

    def test_getattr_with_non_existing_item(self):
        with self.assertRaises(AttributeError):
            self.vault.non_existing_item



class TestFile(unittest.TestCase):
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def save_with_raw_data(self, mock_open, mock_makedirs):
        file = File(None, 'type_key', 'filename', b'raw_data')
        file.save()
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once_with(file.path(), 'wb')

    def save_without_raw_data(self):
        file = File(None, 'type_key', 'filename')
        with self.assertRaises(ValueError):
            file.save()

    def base(self):
        file = File(None, 'type_key', 'filename.ext')
        self.assertEqual(file.base(), 'filename')

    def ext(self):
        file = File(None, 'type_key', 'filename.ext')
        self.assertEqual(file.ext(), 'ext')

    def type(self):
        file = File(None, 'type_key', 'filename.ext')
        self.assertEqual(file.type(), 'type_key')

    def mime(self):
        file = File(None, 'type_key', 'filename.txt')
        self.assertEqual(file.mime(), 'text/plain')