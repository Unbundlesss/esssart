import json
import decimal
from .app import app


class RiffObject:
    _loops = []
    _loop_audio = []
    _riff = None
    _image = None
    _joins = []
    _loop_ids = []

    @staticmethod
    def key_to_type(att):
        key = list(att.keys())[0] if att else None
        obj = {"type": key}

        if key:
            for i in ['endpoint', 'bucket', 'hash', 'key', 'length', 'mime', 'url']:
                obj[i] = att.get(key, {}).get(i)
            obj['hash'] = obj.get('hash', '').strip('"')
            obj['id'] = obj.get('key', '').split("/")[-1]

        return obj

    @staticmethod
    def json_obj(dct):
        # pull loop state
        loop_states = map(
            lambda x: dict(
                gain=x.get('slot', {}).get('current', {}).get('gain', 1),
                on=x.get('slot', {}).get('current', {}).get('on', True)
            ),
            dct.get('state', {}).get('playback', [])
        )
        loop_mains = list(map(
            lambda x: dict(
                id=x.get('_id'),
                app_version=x.get('app_version'),
                audio_attachment_id=None,
                audio_attachment=RiffObject.key_to_type(x.get('cdn_attachments')),
                bar_length=x.get('barLength'),
                bps=x.get('bps'),
                buffer_path=x.get('bufferPath'),
                buffer_url=x.get('bufferURL'),
                colour_history=json.dumps(x.get('colourHistory')),
                created=x.get('created'),
                creator_username=x.get('creatorUserName'),
                is_bass=x.get('isBass', False),
                is_drum=x.get('isDrum', False),
                is_mic=x.get('isMic', False),
                is_normalized=x.get('isNormalized', False),
                is_note=x.get('isNote', False),
                length=x.get('length'),
                length_16ths=x.get('length16ths'),
                max_allowed_peak_level=x.get('maxAllowedPeakLevel'),
                original_pitch=x.get('originalPitch'),
                peak_level=x.get('peakLevel'),
                preset_name=x.get('presetName'),
                primary_color=x.get('primaryColour'),
                sample_rate=x.get('sampleRate')
            ),
            dct.get('loops', []),
        ))

        loop_ordinals = [{"ordinal": i} for i in list(range(0, loop_mains.__len__()))]

        out = dict(
            image_attachment_id=None,
            id=dct.get('doc_id'),
            action_timestamp=dct.get('action_timestamp'),
            action_timestamp_iso=dct.get('action_timestamp_iso'),
            app_version=dct.get('rifff', {}).get('app_version'),
            band=dct.get('band'),
            bar_length=dct.get('rifff', {}).get('state', {}).get('barLength'),
            bps=dct.get('rifff', {}).get('state', {}).get('bps'),
            brightness=dct.get('rifff', {}).get('brightness'),
            color=dct.get('rifff', {}).get('colour'),
            comment_count=dct.get('commentCount', 0),
            comments=json.dumps(dct.get('comments', [])),
            created=dct.get('rifff', {}).get('created'),
            creators=json.dumps(dct.get('creators', [])),
            database_id=dct.get('database_id'),
            image=dct.get('image'),
            image_attachment=RiffObject.key_to_type(dct.get('image_attachment')),
            image_url=dct.get('image_url'),
            layer_colors=json.dumps(dct.get('rifff', {}).get('layerColours', [])),
            likes=json.dumps(dct.get('react_counts', {}).get('like', 0)),
            loop_ids=[],
            loops=map(
                lambda state, main, ordinals: {**main, **state, **ordinals},
                loop_states, loop_mains, loop_ordinals),
            magnitude=dct.get('rifff', {}).get('magnitude', 0.5),
            peak_data=json.dumps(dct.get('rifff', {}).get('peakData', [])),
            private=dct.get('private', False),
            root=dct.get('rifff', {}).get('root'),
            scale=dct.get('rifff', {}).get('scale'),
            sent_by=dct.get('rifff', {}).get('sentBy'),
            title=dct.get('title'),
            user=dct.get('user')
        )
        return out

    def __init__(self, _input):
        self.__dict__ = json.loads(_input, object_hook=self.json_obj, parse_float=decimal.Decimal)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def get_loops(self):
        # see if the loops are cached
        _loops = self.get('_loops', [])
        if not _loops:
            json_loops = self.get('loops', [])
            _audio_loops = list(map(lambda x: self.parse_audio(x), json_loops))
            _loops = list(map(lambda x, y: x.set('audio_attachment_id', y.id), json_loops, _audio_loops))
            app.loop.create_many(_loops)
            if not self._loop_ids:
                self._loop_ids = list(map(lambda x: x.id, _loops))

            self._loops = app.loop.get_these(self._loop_ids)

        return self._loops

    def parse_audio(self, loop):
        """create the audio attach ment for a loop if not exists.
        Return the audio attachment"""
        # if the audio is cached, return it
        if self._loop_audio[loop.ordinal]:
            return self._loop_audio[loop.ordinal]

        # if the attachment_id is not set, then the audio is made
        if loop.get('audio_attachment_id') is None:
            audio = app.attachment.create_attachment(loop.audio_attachment)
            self._loop_audio[loop.ordinal] = audio
            loop.set('audio_attachment_id', audio.id)

        # get the audio attachment
        audio = app.attachment.get_attachment(loop.get('audio_attachment_id'))
        return audio

    def build_riff(self):
        # make image
        fields = {i: self.__dict__.get(i) for i in app.shared_riff.get_fields()}
        db_riff = app.shared_riff.get_by_id(self.get('id'))
        if not db_riff:
            db_riff = app.shared_riff.create_shared_riff(fields)

        image = self.image()
        db_riff.image_attachment = image

        loops = self.get_loops()

        # join loops using join_riff_loop
        app.join_riff_loop.join_loops_to_riff(db_riff, loops)
        db_riff.loops = loops

    def image(self):
        if self._image:
            return self._image
        if self.get("image_attachment_id") is None:
            image = app.attachment.create_attachment(self.get('image_attachment'))
            self.set('image_attachment_id', image.id)
        else:
            image = app.attachment.get_attachment(self.get('image_attachment_id'))

        self._image = image
        return image

    def remove(self, key):
        del self.__dict__[key]

    def set(self, key, value):
        self.__dict__[key] = value
