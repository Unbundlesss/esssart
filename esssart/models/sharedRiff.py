import sqlite3
import json
from collections import namedtuple


class RifffDoc:
    fields =  [ 
                'doc_id TEXT PRIMARY KEY',
                'action_timestamp INTEGER',
                'action_timestamp_iso TEXT',
                'band TEXT',
                'cdn_attachments TEXT',
                'creator_id INTEGER',
                'database_id TEXT',
                'image BOOLEAN',
                'app_version',
                'likes INTEGER',
                'image_url TEXT',
                'private BOOLEAN',
                'riff TEXT',
                'title TEXT',
                'type TEXT',
                'user TEXT',
              ]
    field_names = [field.split()[0] for field in fields]
    foreigns = 'FOREIGN KEY(creator_id) REFERENCES user(_id)'
    # field names and foreigns
    schema = f"CREATE TABLE shared_riff ({', '.join(fields)}), {foreigns}"

    def __init__(self, doc_data, db):
        super().__init__(db)
        self.SharedRiff = namedtuple("SharedRiff", self.field_names)
        self.db = db

    def fromJson(self, doc_data):
        mapping = {}
        mapping.doc_id = doc_data.get("doc_id")
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
        mapping.cdn_attachments = doc_data.get("cdn_attachments", {})
        mapping.image_url = doc_data.get("image_url")
        mapping.image = doc_data.get("image")

        riff = self.SharedRiff(*mapping)

    def persist(self):
        cursor = self.db.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS shared_riff (
                doc_id TEXT PRIMARY KEY,
                user TEXT,
                band TEXT,
                database_id TEXT,
                type TEXT,
                action_timestamp INTEGER,
                action_timestamp_iso TEXT,
                title TEXT,
                private BOOLEAN,
                react_counts TEXT,
                riff TEXT,
                cdn_attachments TEXT,
                image_url TEXT,
                image BOOLEAN,
                creator_id INTEGER,
                FOREIGN KEY(creator_id) REFERENCES user(_id)
            )
        """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS riff_loops (
                doc_id TEXT,
                loop_id TEXT,
                on BOOLEAN,
                gain REAL,
                FOREIGN KEY(doc_id) REFERENCES shared_riff(doc_id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS loops (
                _id TEXT PRIMARY KEY,
                cdn_attachments TEXT,
                isNote BOOLEAN,
                primaryColour TEXT,
                bps REAL,
                app_version INTEGER,
                isMic BOOLEAN,
                bufferURL TEXT,
                colourHistory TEXT,
                isDrum BOOLEAN,
                length16ths INTEGER,
                originalPitch INTEGER,
                creatorUserName TEXT,
                type TEXT,
                length INTEGER,
                presetName TEXT,
                bufferPath TEXT,
                isBass BOOLEAN,
                sampleRate INTEGER,
                barLength INTEGER,
                created INTEGER
            )
        """
        )

        for creator in self.creators:
            if not self.db.User.name_exists(creator):
                self.db.User.name_create(creator)
            creator_id = self.db.User.name_get(creator).id
            break  # Only need one creator for the foreign key

        cursor.execute(
            """
            INSERT OR REPLACE INTO shared_riff (
                doc_id, user, band, database_id, type,
                action_timestamp, action_timestamp_iso, title, private,
                react_counts, riff, cdn_attachments, image_url, image, creator_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                self.doc_id,
                self.user,
                self.band,
                self.database_id,
                self.type,
                self.action_timestamp,
                self.action_timestamp_iso,
                self.title,
                self.private,
                json.dumps(self.react_counts),
                json.dumps(self.riff),
                json.dumps(self.cdn_attachments),
                self.image_url,
                self.image,
                creator_id,
            ),
        )

        playback_data = self.riff.get("state", {}).get("playback", [])
        for loop, playback in zip(self.loops, playback_data):
            cursor.execute(
                """
                INSERT OR REPLACE INTO loops (
                    _id, cdn_attachments, isNote, primaryColour, bps, app_version,
                    isMic, bufferURL, colourHistory, isDrum, length16ths, originalPitch,
                    creatorUserName, type, length, presetName, bufferPath, isBass, sampleRate,
                    barLength, created, 
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    loop["_id"],
                    json.dumps(loop["cdn_attachments"]),
                    loop.get("isNote", False),
                    loop.get("primaryColour"),
                    loop.get("bps"),
                    loop.get("app_version"),
                    loop.get("isMic", False),
                    loop.get("bufferURL", ""),
                    json.dumps(loop.get("colourHistory", [])),
                    loop.get("isDrum", False),
                    loop.get("length16ths"),
                    loop.get("originalPitch"),
                    loop.get("creatorUserName"),
                    loop.get("type"),
                    loop.get("length"),
                    loop.get("presetName", ""),
                    loop.get("bufferPath", ""),
                    loop.get("isBass", False),
                    loop.get("sampleRate"),
                    loop.get("barLength"),
                    loop.get("created"),
                ),
            )

            playback_cleaned = {
                "on": playback.get("slot", {}).get("current", {}).get("on"),
                "gain": playback.get("slot", {}).get("current", {}).get("gain"),
            }
            cursor.execute(
                """
                INSERT INTO riff_loops (doc_id, loop_id, on, gain) VALUES (?, ?, ?, ?)
            """,
                (
                    self.doc_id,
                    loop["_id"],
                    playback_cleaned["on"],
                    playback_cleaned["gain"],
                ),
            )

        self.db.commit()
