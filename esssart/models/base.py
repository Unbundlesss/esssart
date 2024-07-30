from ptpython.utils import ptrepr_to_repr
from prompt_toolkit.formatted_text import HTML
from ..decorators import handle_params
from abc import ABC, abstractmethod

@ptrepr_to_repr
class Base(ABC):
    table = None
    index = []
    extra = []
    fields = []
    app = None

    def __pt_repr__(self):
        qclass = self.__class__.__name__
        table = self.table
        fields = "\n        ".join(self.field_names)
        return HTML(
            f"""\n<yellow>Model: {qclass} </yellow>
<blue>Table: {table}</blue>
Fields: {fields}\n"""
        )

    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()
        if self.extra:
            extras = ", ".join(self.extra) + ", "
        else:
            extras = ""

        if not self.schema:
            self.schema = f"""CREATE TABLE {self.table} (
                {', '.join(self.fields)}
                {extras})"""

        self.field_names = self.get_field_names(self.fields)

    @classmethod
    def set_app(cls, app):
        cls.app = app

    @staticmethod
    def get_field_names(fields):
        return [field.split()[0] for field in fields]

    def get_fields(self):
        return self.get_field_names(self.fields)

    def get_last(self):
        last_id = self.cur.lastrowid
        return self.get_one(last_id)

    def get_one(self, _id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE id = ?", (_id,))
        row = self.cur.fetchone()
        return self.tuple(*row)

    @handle_params
    def add(self, _=None, *args, **qdict):
        qlist = qdict.keys()
        columns = ", ".join(qlist)
        placeholders = ", ".join("?" for _ in qdict)
        values = tuple(qdict.values())
        self.cur.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values
        )
        self.con.commit()

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
        self.cur.execute(
            f"""INSERT INTO {self.table} ({columns}) 
            VALUES ({placeholders}) 
            WHERE NOT EXISTS
            (SELECT 1 FROM {self.table} WHERE {check} = ?)
            """,
            values,
        )
        self.con.commit()

    def colcheck(self, col):
        if col not in self.field_names:
            raise ValueError(f"Invalid column: {col}")

    def get_these(self, ids):
        cur = self.cur
        cur.execute(
            f"SELECT * FROM {self.table} WHERE id IN ({','.join('?' for _ in ids)})",
            (ids,)
        )
        return [self.tuple(*row) for row in cur.fetchall()]

    def get_many(self, param, value, limit=100):
        cur = self.cur
        self.colcheck(param)

        cur.execute(
            f"SELECT * FROM {self.table} WHERE {param} = ? LIMIT ?", (value, limit)
        )
        return [self.tuple(*row) for row in cur.fetchall()]

    def get_all(self):
        cur = self.cur
        cur.execute(f"SELECT * FROM {self.table}")
        rows = cur.fetchall()
        if rows:
            return [self.tuple(*row) for row in rows]
        return []

    def name_create_many(self, users):
        self.cur.executemany(
            "INSERT OR IGNORE INTO user (username) VALUES (?)", users
        )
        self.con.commit()

    def get_custom(self, param, value, asdict=False):
        cur = self.cur
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

        self.cur.execute(
            f"UPDATE {self.table} SET {set_clause} WHERE id = ?",
            values + (id,),
        )
        self.con.commit()

    def delete(self, id):
        if not id:
            raise ValueError("Primary key 'id' must be provided for delete")

        self.cur.execute(f"DELETE FROM {self.table} WHERE id = ?", (id,))
        self.con.commit()

    def init(self):
        cmds = self.get_schema()
        for cmd in cmds:
            self.cur.execute(cmd)
            self.con.commit()
