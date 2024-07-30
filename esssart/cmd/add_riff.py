from ..riffObject import RiffObject
from .. import db


def add_riff(obj: RiffObject):
    # get image

    # make into attachment, get id
    image = db.attachment.create_attachment(obj.image())

    # attach image to riff via id


    # get loops

    # loop through loops and create attachment for each, get id

    # attach audio to loop by adding audio attachment id to loop

    # create loop  in db, collect list of them

    # create riff

    # join riff to loops in db via Join RiffLoop





    # get riff
    riff = obj.riff()
    # get loops
    loops = obj.loops()



    # create riff in db
