from collections import namedtuple


class User:
    schema = "CREATE TABLE user (id INTEGER PRIMARY KEY, username TEXT, avatar TEXT, UNIQUE(username))"

    def __init__(self, db):
        self.db = db
        self.User = namedtuple("User", ["id", "username", "avatar"])

    def name_create_many(self, users):
        self.db.cursor().executemany("INSERT OR IGNORE INTO user (username, avatar) VALUES (?, ?)", users)
        self.db.commit()

    def name_create(self, name):
        self.db.cursor().execute("INSERT OR IGNORE INTO user  (username, avatar)  VALUES (?, ?)", (name, ""))
        self.db.commit()

    def name_avatar(self, name, avatar):
        self.db.cursor().execute("UPDATE user SET avatar = ? WHERE username = ?", (avatar, name))
        self.db.commit()

    def has_avatar(self, name):
        cur = self.db.cursor().execute("SELECT user, avatar FROM user WHERE username = ?", (name,))
        if cur.rowcount > 0:
            if cur.fetchOne().avatar != "":
                return True
            else:
                return False

    def name_exists(self, name):
        cur = self.db.cursor().execute("SELECT * FROM user WHERE username = ?", (name,))
        if cur.rowcount > 0:
            return True
        return False

    def name_get(self, name):
        cur = self.db.cursor().execute("SELECT * FROM user WHERE username = ?",(name,))
        if cur.rowcount > 0:
            u = cur.fetchOne()
            return self.User(id=u.id,avatar=u.avatar,username=u.username)

    def get_missing(self):
        cur = self.db.cursor().execute("SELECT username FROM user WHERE avatar = ?", ("",))
        _all = cur.fetchall()
        rem = [u[0] for u in _all]
        return rem
