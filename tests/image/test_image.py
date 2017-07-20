import autoswatch

import io
import json
import hashlib
import PIL.Image

from collections import OrderedDict

from nose.tools import assert_equals

class TestImage:

    def test_defaults(self):
        """
        Assert that an Image is created with defaults: …
        a size of 20x20 in the form of a tuple, a default color string
        of the hex value #ffffff, a default color mode of 'RGB', and a
        default format of 'PNG'.
        """
        i = autoswatch.Image()
        assert_equals(i.size,   (20, 20))
        assert_equals(i.color,  '#ffffff')
        assert_equals(i.mode,   'RGB')
        assert_equals(i.format, 'PNG')

    def test_constructor(self):
        """
        Assert that an Image is created with a size, color, mode and format.
        """
        i = autoswatch.Image((40, 40), '#ff0000', 'RGBA', 'JPG')
        assert_equals(i.size,   (40, 40))
        assert_equals(i.color,  '#ff0000')
        assert_equals(i.mode,   'RGBA')
        assert_equals(i.format, 'JPG')

    def test_named_params(self):
        """
        Assert that an Image can accept named params.
        """
        i_size   = autoswatch.Image(size=(40, 40))
        i_color  = autoswatch.Image(color='#ff0000')
        i_mode   = autoswatch.Image(image_mode='RGBA')
        i_format = autoswatch.Image(image_format='JPG')

        assert_equals(i_size.size,     (40, 40))
        assert_equals(i_color.color,   '#ff0000')
        assert_equals(i_mode.mode,     'RGBA')
        assert_equals(i_format.format, 'JPG')

    def test_to_odict(self):
        """
        Assert #to_odict returns a well-ordered dictionary representation.
        Well-ordered means the keys are alphabetized, and the
        representation is meant to be turned into JSON, so all the values
        are strings. Returns and OrderedDict to preserve order.
        """
        i = autoswatch.Image()
        d = {
            'size':   '20x20',
            'color':  '#ffffff',
            'mode':   'RGB',
            'format': 'PNG'
        }
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

        # https://docs.python.org/3.6/library/collections.html#collections.OrderedDict
        assert_equals(list(i.to_odict().items()), list(d.items()))

    def test_guid(self):
        """
        Assert #uid returns a hashed representation of the instance.
        That representation comes from concatenation the keys of the
        instance's #to_odict method, and then running through a hashing
        algorithm.
        """
        i = autoswatch.Image()
        s = '#ffffffPNGRGB20x20'
        u = hashlib.md5(s.encode('utf-8')).hexdigest()
        assert_equals(i.guid(), u)

    def test_json_serialization(self):
        """
        Assert #to_json returns a well structured JSON representation.
        """
        i = autoswatch.Image()
        j = json.dumps({
            'guid':   i.guid(),
            'size':   '20x20',
            'color':  '#ffffff',
            'mode':   'RGB',
            'format': 'PNG'
        }, sort_keys=True)
        assert_equals(i.to_json(), j)

    def test_byte_stream(self):
        """
        Assert #byte_stream returns the image as a bytes IO buffer.
        """
        i = autoswatch.Image()
        p = PIL.Image.new(
            size=(20,20),
            color='#ffffff',
            mode='RGB'
        )

        with io.BytesIO() as byte_stream:
           p.save(byte_stream, format='PNG')
           assert_equals(
               i.byte_stream().getvalue(),
               byte_stream.getvalue()
           )

    def test_bytes(self):
        """
        Assert #bytes returns the image as a bytes string.
        """
        i = autoswatch.Image()
        p = PIL.Image.new(
            size=(20,20),
            color='#ffffff',
            mode='RGB'
        )

        with io.BytesIO() as byte_stream:
           p.save(byte_stream, format='PNG')
           assert_equals(
               i.bytes(),
               byte_stream.getvalue()
           )

