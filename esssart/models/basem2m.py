from collections import namedtuple
from .base import Base


class BaseM2M(Base):
    foreign_keys = []
    table = None

    def __init__(self, con):
        if self.foreign_keys:
            extra = [f"FOREIGN KEY({k}_id) REFERENCES {k}(id)" for k in self.foreign_keys]
            self.extra = self.extra + extra

        super().__init__(con)

    def join(self, table1, table_id1, table2, table_id2, data={}):
        cur = self.cursor()
        names = [f"{table1}_id", f"{table2}_id"] + list(data.keys())
        values = [table_id1, table_id2] + list(data.values())
        placeholders = ", ".join(["?" for _ in values])
        cur.execute(
            f"""INSERT OR REPLACE into {self.table}({', '.join(names)}) values({placeholders})""",
            (values,),
        )

    def get_related(self, local_id, local=None, foreign=None):
        local_table = self.foreign_keys[0] if local is None else local
        foreign_table = self.foreign_keys[1] if foreign is None else foreign
        join_table = self.table
        cur = self.cur.execute(
            f"""SELECT * from {join_table}
            INNER JOIN {foreign_table} ON {foreign_table}.id = {join_table}.{foreign_table}_id
            WHERE {join_table}.{local_table}_id = ?""",
            (local_id,),
        )
        return [row for row in cur.fetchall()]
