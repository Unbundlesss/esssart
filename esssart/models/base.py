from ptpython.utils import ptrepr_to_repr
from prompt_toolkit.formatted_text import HTML
from ..decorators import handle_params


@ptrepr_to_repr
class Base:
    table = None
    index = []
    schema = None
    extra = []
    fields = []
    tuple = None

    def __pt_repr__(self):
        qclass = self.__class__.__name__
        table = self.table
        fields = "\n        ".join(self.field_names)
        return HTML(
            f"""<yellow>Model: {qclass} </yellow>
<blue>Table: {table}</blue>
Fields: {fields}\n"""
        )

    def __init__(self, db):
        if self.extra:
            extras = ", ".join(self.extra) + ", "
        else:
            extras = ""

        if not self.schema:
            self.schema = f"""CREATE TABLE {self.table} (
                {', '.join(self.fields)}
                {extras})"""

        self.field_names = self.get_field_names(self.fields)
        self.db = db

    @staticmethod
    def get_field_names(fields):
        return [field.split()[0] for field in fields]

    def get_fields(self):
        return self.get_field_names(self.fields)

    def get_last(self):
        last_id = self.db.cur.lastrowid
        return self.get_one(last_id)

    def get_one(self, _id):
        self.db.cur.execute(f"SELECT * FROM {self.table} WHERE id = ?", (_id,))
        row = self.db.cur.fetchone()
        return self.tuple(*row)

    @handle_params
    def add(self, _=None, *args, **qdict):
        qlist = qdict.keys()
        columns = ", ".join(qlist)
        placeholders = ", ".join("?" for _ in qdict)
        values = tuple(qdict.values())
        self.db.cur.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values
        )
        self.db.commit()

    def whitelist(self, ql):
        for key in ql:
            if key not in self.field_names:
                return False
        return True

    @handle_params
    def add_if_not_exist(self, check, *args, **qdict):
        qlist = list(qdict.keys())
        columns = ", ".join(qlist)
        placeholders = ", ".join("?" for _ in qdict)
        values = [qdict.values(), check]
        self.db.cur.execute(
            f"""INSERT INTO {self.table} ({columns}) 
            VALUES ({placeholders}) 
            WHERE NOT EXISTS
            (SELECT 1 FROM {self.table} WHERE {check} = ?)
            """,
            values,
        )
        self.db.commit()

    def colcheck(self, col):
        if col not in self.field_names:
            raise ValueError(f"Invalid column: {col}")

    def get_many(self, param, value, limit=100):
        cur = self.db.cur
        self.colcheck(param)

        cur.execute(
            f"SELECT * FROM {self.table} WHERE {param} = ? LIMIT ?", (value, limit)
        )
        return [self.tuple(*row) for row in cur.fetchall()]

    def get_all(self):
        cur = self.db.cur
        cur.execute(f"SELECT * FROM {self.table}")
        rows = cur.fetchall()
        if rows:
            return [self.tuple(*row) for row in rows]
        return []

    def name_create_many(self, users):
        self.db.cur.executemany(
            "INSERT OR IGNORE INTO user (username) VALUES (?)", users
        )
        self.db.commit()

    def get_custom(self, param, value, asdict=False):
        cur = self.db.cur
        self.colcheck(param)
        values = (value,)
        cur.execute(f"SELECT * from {self.table} WHERE {param} = ?", values)
        row = cur.fetchone()
        if asdict:
            return dict(zip(self.field_names, row))
        else:
            return self.tuple(*row)

    def get_schema(self):
        extra = f" " + ", ".join(self.extra) if self.extra else ""
        if self.index:
            index = [f"CREATE INDEX {index};" for index in self.index]
            return [f"""{self.schema}{extra}""", *index]
        else:
            return [f"""{self.schema}{extra}"""]

    def update(self, id, **kwargs):
        if not self.whitelist(kwargs.keys()):
            raise ValueError("Invalid column in update parameters")

        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = (*kwargs.values(),)

        if not id:
            raise ValueError("Primary key 'id' must be provided for update")

        self.db.cur.execute(
            f"UPDATE {self.table} SET {set_clause} WHERE id = ?",
            values + (id,),
        )
        self.db.commit()

    def delete(self, id):
        if not id:
            raise ValueError("Primary key 'id' must be provided for delete")

        self.db.cur.execute(f"DELETE FROM {self.table} WHERE id = ?", (id,))
        self.db.commit()

    def init(self):
        cmds = self.get_schema()
        for cmd in cmds:
            self.db.cur.execute(cmd)
            self.db.commit()
