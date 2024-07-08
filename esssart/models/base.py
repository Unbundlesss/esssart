from collections import namedtuple


class Base:
    tuple = None
    table = None
    index = []
    schema = None
    extra = []
    fields = []

    def __init__(self, db):
        if self.extra:
            extras = ', '.join(self.extra) + ', '
        else:
            extras = ''

        if not self.schema:
            self.schema = f"""
                CREATE TABLE {self.table} (
                {', '.join(self.fields)}
                {extras})"""

        self.field_names = self.get_field_names(self.fields)
        self.db = db

    @staticmethod
    def get_field_names(fields):
        return [field.split()[0] for field in fields]

    def get_last(self):
        last_id = self.db.cursor().lastrowid
        return self.get_one(last_id)

    def get_one(self, _id):
        self.db.cursor().execute(
            f"SELECT * FROM {self.table} WHERE id = ?", (_id,)
        )
        row = self.db.cursor().fetchone()
        return self.tuple(*row)

    def add(self, qdict=None, **kwargs):
        if qdict is None:
            qdict = kwargs
        columns = ", ".join(qdict.keys())
        placeholders = ", ".join("?" for _ in qdict)
        values = tuple(qdict.values())
        self.db.cursor().execute(
            f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values
        )
        self.db.commit()

    def get_many(self, param, value, limit=100):
        cur = self.db.cursor()
        values = tuple(param, value, limit)
        condition = f"WHERE ? = ?"
        limit = f"LIMIT ?"
        cur.execute(f"SELECT * FROM {self.table} {condition} {limit}", values)
        return [self.tuple(*row) for row in cur.fetchall()]

    def name_create_many(self, users):
        self.db.cursor().executemany("INSERT OR IGNORE INTO user (username) VALUES (?)", users)
        self.db.commit()

    def get_custom(self, param, value):
        cur = self.db.cur
        values = tuple(param, value)
        cur.execute(f"SELECT * from {self.table} WHERE ? = ?", values)
        return self.tuple(*cur.fetchOne())

    def get_schema(self):
        if self.index:
            index = ','.join(["CREATE INDEX {index};" for index in self.index])
            return f"""\
                {self.schema};
                {index}"""
        else:
            return f"""{self.schema}""";

    def init(self):
        cur = self.db.cursor()
        cur.execute(self.get_schema())
        cur.commit()
