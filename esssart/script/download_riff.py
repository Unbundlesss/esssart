import requests
import os
from .. import app
from multiprocessing import Pool
import json
import time

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

def digest_riff(riff):
    # get the vault
    stash = app.vault.stem

    # convert riff from json to Riff object by separating the loops and cdn_attachments out


    # get the loops for the riff
    loops = app.riff.get_loops(riff.id)

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

    # update the app with local paths
    app.riff.update_local(riff_file.path(), riff.id)
    for loop, loop_file in zip(loops, loop_files):
        app.loop.update_local(loop_file.path(), loop.id)

    return riff.id


def download_attachment(_id):
    # get the vault
    stash = app.vault.stem
    # get attachment from app
    att = app.attachment.get_attachment(_id)
    # download the file
    resp = s.get(att.url)

    # save the file to disk
    file = stash(att, resp.content)
    file.save()

    # update app with local path
    app.attachment.update_local(file.path(), att.key)
