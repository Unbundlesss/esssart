import os
import sqlite3
from pathlib import Path
from collections import namedtuple
from .user import User

dbpath = Path.home() / ".esssart.database.db"

is_new = True if not os.path.exists(dbpath) else False
con = sqlite3.connect(dbpath)
cur = con.cursor()

if is_new:
    cur.execute(User.schema)

user = User(con)

db = namedtuple('dbconnection', 'con user')(con=con, user=user)
