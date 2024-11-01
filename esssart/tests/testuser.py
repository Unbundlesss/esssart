import unittest
from unittest.mock import Mock
from esssart.models.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.mock_con = Mock()
        self.mock_cur = Mock()
        self.mock_con.cursor.return_value = self.mock_cur
        self.user = User(self.mock_con)

    def name_create_creates_user(self):
        name = "testuser"
        self.user.add = Mock()
        self.user.name_create(name)
        self.user.add.assert_called_once_with({name: name})

    def name_avatar_updates_avatar(self):
        name = "testuser"
        avatar = "avatar.png"
        self.user.cur.execute = Mock()
        self.user.con.commit = Mock()
        self.user.name_avatar(name, avatar)
        self.user.cur.execute.assert_called_once_with(
            "UPDATE user SET avatar = ? WHERE username = ?", (avatar, name)
        )
        self.user.con.commit.assert_called_once()

    def has_avatar_returns_true_if_user_has_avatar(self):
        name = "testuser"
        self.user.cur.execute = Mock(return_value=self.user.cur)
        self.user.cur.rowcount = 1
        self.user.cur.fetchOne = Mock(return_value=Mock(avatar="avatar.png"))
        result = self.user.has_avatar(name)
        self.assertTrue(result)

    def has_avatar_returns_false_if_user_has_no_avatar(self):
        name = "testuser"
        self.user.cur.execute = Mock(return_value=self.user.cur)
        self.user.cur.rowcount = 1
        self.user.cur.fetchOne = Mock(return_value=Mock(avatar=""))
        result = self.user.has_avatar(name)
        self.assertFalse(result)

    def has_avatar_raises_error_if_user_not_found(self):
        name = "testuser"
        self.user.cur.execute = Mock(return_value=self.user.cur)
        self.user.cur.rowcount = 0
        with self.assertRaises(ValueError):
            self.user.has_avatar(name)

    def name_exists_returns_true_if_user_exists(self):
        name = "testuser"
        self.user.cur.execute = Mock(return_value=self.user.cur)
        self.user.cur.rowcount = 1
        result = self.user.name_exists(name)
        self.assertTrue(result)

    def name_exists_returns_false_if_user_does_not_exist(self):
        name = "testuser"
        self.user.cur.execute = Mock(return_value=self.user.cur)
        self.user.cur.rowcount = 0
        result = self.user.name_exists(name)
        self.assertFalse(result)

    def name_to_id_returns_id_if_user_exists(self):
        name = "testuser"
        user_id = 1
        self.user.cur.execute = Mock(return_value=self.user.cur)
        self.user.cur.fetchone = Mock(return_value=(user_id,))
        result = self.user.name_to_id(name)
        self.assertEqual(result, (user_id,))

    def name_to_id_returns_none_if_user_does_not_exist(self):
        name = "testuser"
        self.user.cur.execute = Mock(return_value=self.user.cur)
        self.user.cur.fetchone = Mock(return_value=None)
        result = self.user.name_to_id(name)
        self.assertIsNone(result)

    def name_get_returns_user_if_exists(self):
        name = "testuser"
        user_data = {"username": name, "avatar": "avatar.png"}
        self.user.get_custom = Mock(return_value=user_data)
        result = self.user.name_get(name)
        self.assertEqual(result, user_data)

if __name__ == "__main__":
    unittest.main()