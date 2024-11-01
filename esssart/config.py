import os
from typing import NamedTuple

from appdirs import AppDirs
from collections import namedtuple


def make_config(base_dir=None, db_file_name=None):
    appdirs = AppDirs("esssart", "esssart")
    base_dir_default = appdirs.user_data_dir

    base_dir = os.path.realpath(base_dir) if base_dir is not None else base_dir_default

    _data_paths = {
        "json": "json",
        "db": "db",
        "avatar": f"image{os.path.pathsep}avatar",
        "cover": f"image{os.path.pathsep}cover",
        "banner": f"image{os.path.pathsep}banner",
        "stem": f"attachment{os.path.pathsep}stem",
        "temp": ".temp",
    }

    data_paths = dict()

    for i in _data_paths:
        data_paths[i] = os.path.join(base_dir, data_paths[i])

    if db_file_name is not None:
        db_file_name = (
            "".join(
                e for e in db_file_name if e.isalnum() or (e == "." or e == "_")
            ).strip(".")
            or None
        )
        db_file_name = (
            db_file_name if db_file_name is not None else "esssart.database.db"
        )
    else:
        db_file_name = "esssart.database.db"

    dbname = os.path.join(data_paths["db"], db_file_name)

    endlesss_auth = {"Authorization": "Bearer "}

    out = dict(
        datapaths=data_paths,
        dbpath=dbname,
    )

    c = namedtuple("Config", out.keys())
    out2 = c(**out)
    return out2

