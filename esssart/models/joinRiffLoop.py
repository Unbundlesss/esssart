from collections import namedtuple

from .loop import Loop
from .basem2m import BaseM2M


class JoinRiffLoop(BaseM2M):
    fields = [
        "shared_riff_id TEXT",
        "loop_id TEXT",
        "gain REAL",
        "is_on BOOLEAN",
        "ordinal INTEGER",
    ]
    foreign_keys = ["shared_riff", "loop"]
    table = "join_riff_loop"
    index = [f"shared_riff_loop_idx on {table}(shared_riff_id, loop_id)"]

    def __init__(self, con):
        super().__init__(con)
        self.JoinRiffLoop = namedtuple(
            "JoinRiffLoop", self.field_names + Loop.get_field_names(Loop.fields)
        )
        self.tuple = self.JoinRiffLoop

    def get_related_loops(self, shared_riff_id):
        return [
            self.JoinRiffLoop(row) for row in self.get_related(self, shared_riff_id)
        ]

    def join_loops_to_riff(self, riff, loops):
        for loop in loops:
            res = self.cur.execute(
                f"SELECT * from {self.table} where shared_riff_id = ? and loop_id = ?",
                (riff.id, loop.id),
            )
            if res.fetchone():
                continue

            self.add(
                {
                    "shared_riff_id": riff.id,
                    "loop_id": loop.id,
                    "gain": loop.gain,
                    "is_on": loop.on,
                    "ordinal": loop.ordinal,
                }
            )
