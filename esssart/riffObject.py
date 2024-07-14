import json
import decimal


class RiffObject:
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
    def as_obj(dct):
        # pull loop state
        loop_states = map(
            lambda x: dict(
                gain=x.get('slot', {}).get('current', {}).get('gain', 1),
                on=x.get('slot', {}).get('current', {}).get('on', True)
            ),
            dct.get('state', {}).get('playback', [])
        )
        loop_mains = map(
            lambda x: dict(
                id=x.get('_id'),
                app_version=x.get('app_version'),
                attachment=x.get('cdn_attachments'),
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
        )

        out = dict(
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
            loops=map(lambda state, main: {**main, **state}, loop_states, loop_mains),
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
        self.__dict__ = json.loads(_input, object_hook=self.as_obj, parse_float=decimal.Decimal)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def get(self, key):
        return self.__dict__.get(key)
