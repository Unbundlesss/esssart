from collections import namedtuple
from .base import Base


class User(Base):
    fields = ["id INTEGER PRIMARY KEY", "username TEXT UNIQUE", "avatar TEXT"]
    table = "user"
    index = ["username on user(username)"]

    def __init__(self, con):
        super().__init__(con)
        self.User = namedtuple("User", self.field_names)
        self.tuple = self.User

    # def name_create_many(self, users: list[tuple[str, any]]):
    #     self.cursor().executemany("INSERT OR IGNORE INTO user (username, avatar) VALUES (?, ?)", users)
    #     self.con.commit()

    def name_create(self, name):
        self.add({name: name})

    def name_avatar(self, name, avatar):
        self.cur.execute(
            "UPDATE user SET avatar = ? WHERE username = ?", (avatar, name)
        )
        self.con.commit()

    def has_avatar(self, name):
        cur = self.cur.execute(
            "SELECT username, avatar FROM user WHERE username = ?", (name,)
        )
        if cur.rowcount > 0:
            if cur.fetchOne().avatar != "":
                return True
            else:
                return False
        raise ValueError("User not found")

    def name_exists(self, name):
        cur = self.cur.execute("SELECT * FROM user WHERE username = ?", (name,))
        if cur.rowcount > 0:
            return True
        return False

    def name_to_id(self, name):
        cur = self.cur.execute("SELECT id FROM user WHERE username = ?", (name,))
        return cur.fetchone()

    def name_get(self, name):
        return self.get_custom("name", name)

    # def get_missing(self):
    #     cur = self.cur.execute("SELECT username FROM user WHERE avatar = ?", ("",))
    #     _all = cur.fetchall()
    #     rem = [u[0] for u in _all]
    #     return rem
