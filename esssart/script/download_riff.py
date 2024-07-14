import requests
import os
from .. import db
from multiprocessing import Pool
import json
import time

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

def digest_riff(riff):
    # get the vault
    stash = db.vault.stem

    # convert riff from json to Riff object by separating the loops and cdn_attachments out


    # get the loops for the riff
    loops = db.riff.get_loops(riff.id)

    # create a folder for the riff
    folder = stash.folder("riff", riff.id)

    # create a folder for the loops
    loop_folder = stash.folder("loop", riff.id)

    # download the riff
    download_attachment(riff.id)

    # download the loops
    with Pool(4) as p:
        p.map(download_attachment, [loop.id for loop in loops])

    # save the riff and loops to the vault
    riff_file = stash.file("riff", riff.id, riff.id + ".json")
    riff_file.save(riff)
    loop_files = [
        stash.file("loop", riff.id, loop.id + ".json")
        for loop in loops
    ]
    for loop, loop_file in zip(loops, loop_files):
        loop_file.save(loop)

    # update the db with local paths
    db.riff.update_local(riff_file.path(), riff.id)
    for loop, loop_file in zip(loops, loop_files):
        db.loop.update_local(loop_file.path(), loop.id)

    return riff.id


def download_attachment(_id):
    # get the vault
    stash = db.vault.stem
    # get attachment from db
    att = db.attachment.get_attachment(_id)
    # download the file
    resp = s.get(att.url)

    # save the file to disk
    file = stash(att, resp.content)
    file.save()

    # update db with local path
    db.attachment.update_local(file.path(), att.key)
