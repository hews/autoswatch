import PIL

import hashlib
from collections import OrderedDict
from functools import reduce

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

    def uid(self):
        basic_id = ''.join(self.to_odict().values())
        uid = hashlib.md5(basic_id.encode('utf-8')).hexdigest()
        return uid

