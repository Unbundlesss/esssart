import unittest
from unittest.mock import MagicMock
from esssart.models.riff import SharedRiff



class TestSharedRiff(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.shared_riff = SharedRiff(self.mock_db)

    def test_initialization(self):
        self.assertIsInstance(self.shared_riff, SharedRiff)

    def test_add_loop_exists(self):
        self.assertTrue(hasattr(self.shared_riff, 'add_loop'))

    def test_get_loops(self):
        self.mock_db.shared_riff_loop.get_related_loops.return_value = ['loop1', 'loop2']
        loops = self.shared_riff.get_loops('some_id')
        self.assertEqual(loops, ['loop1', 'loop2'])

    def test_get_riff(self):
        self.mock_db.get_custom.return_value = {'id': 'some_id'}
        riff = self.shared_riff.get_riff('some_id')
        self.assertEqual(riff, {'id': 'some_id'})

    def test_get_riff_with_loops(self):
        self.mock_db.get_custom.return_value = {'id': 'some_id', 'riff': 'Cool Riff'}
        self.mock_db.shared_riff_loop.get_related_loops.return_value = ['loop1', 'loop2']
        riff_with_loops = self.shared_riff.get_riff_with_loops('some_id')
        self.assertEqual(riff_with_loops.riff, {'id': 'some_id', 'riff': 'Cool Riff'})
        self.assertEqual(riff_with_loops.loops, ['loop1', 'loop2'])



if __name__ == '__main__':
    unittest.main()