from collections import namedtuple
from . import Loop
from .base import Base


class SharedRiff(Base):
    extra = []
    table = "shared_riff"
    fields = [
        "id TEXT PRIMARY KEY",
        "user_id TEXT",
        "action_timestamp INTEGER",
        "action_timestamp_iso TEXT",
        "app_version TEXT",
        "band TEXT",
        "bar_length INTEGER",
        "bps STRING",
        "brightness REAL",
        "color TEXT",
        "contributors TEXT",
        "created integer",
        "creators BLOB",
        "database_id TEXT",
        "image BOOLEAN",
        "attachment_id TEXT",
        "image_url TEXT",
        "layer_colors BLOB",
        "likes INTEGER",
        "magnitude STRING",
        "peak_data BLOB",
        "private BOOLEAN",
        "riff TEXT",
        "root INTEGER",
        "scale INTEGER",
        "sent_by TEXT",
        "title TEXT",
        "type TEXT",
        "user TEXT"
        'comment_count INTEGER',
        'comments TEXT',
        'magnitude REAL',
        'private BOOLEAN'
    ]
    index = [
        "shared_riff_id_user_id ON shared_riff(id, user_id)",
        "shared_riff_creator_id ON shared_riff(creator_id)",
        "shared_riff_time ON shared_riff(action_timestamp)",
        "shared_riff_time_iso ON shared_riff(action_timestamp_iso)"
    ]

    def __init__(self, db):
        super().__init__(db)
        self.SharedRiff = namedtuple(
            "SharedRiff",
            self.field_names,
        )
        self.SharedRiffWithLoops = namedtuple(
            "SharedRiffWithLoops", self.field_names + ["loops"]
        )
        self.tuple = self.SharedRiff

    def add_loop(self, riff, loop):
        pass

    def get_loops(self, shared_riff_id):
        return self.db.shared_riff_loop.get_related_loops(shared_riff_id)

    def get_riff(self, shared_riff_id):
        return self.get_custom("id", shared_riff_id)

    def get_riff_dict(self, shared_riff_id):
        return self.get_custom("id", shared_riff_id, True)



    def get_mapping(self, doc_data):
        mapping = {}
        mapping.id = doc_data.get("doc_id")
        mapping.user = doc_data.get("user")
        mapping.band = doc_data.get("band")
        mapping.database_id = doc_data.get("database_id")
        mapping.type = doc_data.get("type")
        mapping.action_timestamp = doc_data.get("action_timestamp")
        mapping.action_timestamp_iso = doc_data.get("action_timestamp_iso")
        mapping.title = doc_data.get("title")
        mapping.private = doc_data.get("private")
        mapping.creators = doc_data.get("creators", [])
        mapping.react_counts = doc_data.get("react_counts", {})
        mapping.riff = doc_data.get("rifff", {})
        mapping.loops = doc_data.get("loops", [])
        mapping.image_attachment = doc_data.get("image_attachment", {})
        mapping.image_url = doc_data.get("image_url")
        mapping.image = doc_data.get("image")

        mapping.app_version = doc_data.get("app_version")
        mapping.brightness = doc_data.get("brightness")
        mapping.colour = doc_data.get("colour")
        mapping.created = doc_data.get("created")
        mapping.layer_colours = doc_data.get("layerColours")
        mapping.magnitude = doc_data.get("magnitude")
        mapping.peak_data = doc_data.get("peakData")
        mapping.root = doc_data.get("root")
        mapping.scale = doc_data.get("scale")
        mapping.sent_by = doc_data.get("sentBy")
        mapping.bar_length = doc_data.get("barLength")
        mapping.bps = doc_data.get("bps")
        mapping.type = doc_data.get("type")
        mapping.user_name = doc_data.get("user_name")
        mapping.title = doc_data.get("title")
        mapping.type = doc_data.get("type")
        mapping.user = doc_data.get("user")
    def goops(self, _id):
        riff = self.get_riff_dict(_id)
        riff.loops = self.get_loops(_id)
        return self.SharedRiffWithLoops(riff)
