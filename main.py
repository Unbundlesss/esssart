import argparse
import sys
from esssart.sources import pull_sources_list, seed_db
from esssart.avatars import avatars
from esssart.db import db

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
    args = parser.parse_args(argsv)
    if args.cmd == "create":
        pull_sources_list()
        seed_db()

    if args.cmd == "avatars":
        avatars(limit=args.limit, start=args.start)

if __name__ == "__main__":
    main(sys.argv[1:])
