
import io
import json
import hashlib
import PIL.Image

from collections import OrderedDict

class Image:
    def __init__(self, size=(20,20), color='#ffffff', image_mode='RGB', image_format='PNG'):
        # ^#(?:[0-9a-fA-F]{1,2}){3}$ <-- Hex color code def…

        self.size   = size
        self.color  = color
        self.mode   = image_mode
        self.format = image_format

    def to_odict(self):
        return OrderedDict([
            ('color',  self.color),
            ('format', self.format),
            ('mode',   self.mode),
            ('size',   'x'.join(map(str, self.size)))
        ])

    def to_json(self):
        odict = self.to_odict()
        odict['guid'] = self.guid()
        return json.dumps(odict, sort_keys=True)

    def guid(self):
        basic_id = ''.join(self.to_odict().values())
        uid = hashlib.md5(basic_id.encode('utf-8')).hexdigest()
        return uid

    def byte_stream(self):
        i = PIL.Image.new(
            size=self.size,
            color=self.color,
            mode=self.mode
        )
        byte_stream = io.BytesIO()
        i.save(byte_stream, format=self.format)
        byte_stream.seek(0)
        return byte_stream

    def bytes(self):
        byte_stream = self.byte_stream()
        bytes_value = byte_stream.getvalue()
        byte_stream.close()

        return bytes_value
