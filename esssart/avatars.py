import requests
import json
import os
from .db import db
from .crop import crop_to_square
from multiprocessing import Pool
import time

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})


def pull_file(imgset):
    file1, file2, name, url = imgset
    data = s.get(url).content
    with open(file1, "wb") as file:
        file.write(data)
        print(f"{file1} pulled")
    db.user.name_avatar(name, file1)


def process1(plist):
    with Pool() as pool:
        pool.map(pull_file, plist)
        pool.map(crop_to_square, plist)

def avatars(limit: int = 10, start: int = 0):
    try:
        os.makedirs("avatars", exist_ok=True)
    except:
        print("Directory does not exist and can't be made")
        exit()
    print('running')

    avatar_list = db.user.get_missing()
    _iter = 0
    _relstart=0
    _reljump=10
    processlist = []
    for av in avatar_list:
        if _iter >= limit:
            break
        resp = s.get(f"https://api.endlesss.fm/accounts/{av}/avatar", allow_redirects=False)
        redir = s.get_redirect_target(resp)
        if not redir:
            print(f'Error getting avatar for user {av}')
            continue
        if redir.split("/")[-1] == 'default_avatar_2x.png':
            print("default avatar")
            db.user.name_avatar(av, 'default_avatar_2x.png')
            continue
        print(f"{_iter=} {av=}")
        _iter += 1
        processlist.append((f"avatars/{av}.jpg", f"avatars/{av}_processed.jpg", av, redir))
        if _iter > 0 and _iter % _reljump == 0:
            print('sending chunk to queue')
            process1(processlist[_relstart:(_relstart + _reljump)])
            _relstart = _relstart +_reljump
