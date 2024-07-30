import unittest
from unittest.mock import Mock
from esssart.models.loop import Loop

class TestLoop(unittest.TestCase):
    def setUp(self):
        self.mock_con = Mock()
        self.mock_cur = Mock()
        self.mock_con.cursor.return_value = self.mock_cur
        self.loop = Loop(self.mock_con)

    def test_create_loop(self):
        loop_data = {
            "id": "loop1",
            "app_version": 1,
            "bar_length": 4,
            "username": "user1",
            "creator_id": 123,
            "bps": "120",
            "instrument": "guitar",
            "buffer_path": "/path/to/buffer",
            "buffer_url": "http://example.com/buffer",
            "created": 1620000000,
            "color_history": b"\x00\x01",
            "audio_attachment_id": 456,
            "creator_username": "creator1",
            "is_bass": False,
            "is_drum": True,
            "is_mic": False,
            "is_normalized": True,
            "is_note": False,
            "length": 16,
            "length_16ths": 64,
            "original_pitch": 0,
            "preset_name": "preset1",
            "primary_colour": "red",
            "sample_rate": 44100,
        }
        self.loop.add = Mock()
        self.loop.get_last = Mock(return_value=loop_data)
        result = self.loop.create_loop(loop_data)
        self.loop.add.assert_called_once_with(loop_data)
        self.assertEqual(result, loop_data)

if __name__ == "__main__":
    unittest.main()