import argparse
import sys
from ptpython.ipython import embed

from esssart import db

# from esssart.sources import pull_sources_list, seed_db
# from esssart.avatars import avatars
# from esssart.riff_pics import request_riffs, request_liked_riffs


def main(argsv):
    parser = argparse.ArgumentParser(description="run command.")
    parser.add_argument("cmd", type=str, help="the command")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        required=False,
        help="limit the number of whatever",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        required=False,
        help="starting point of the list",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        required=False,
        help="load file when needed"
    )
    args = parser.parse_args(argsv)

    if args.cmd == "shared":
        pass

    if args.cmd == "seed":
        pass

    if args.cmd == "cli":
        embed()


if __name__ == "__main__":
    main(sys.argv[1:])
