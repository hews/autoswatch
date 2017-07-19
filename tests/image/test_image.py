from nose.tools import assert_equals
import autoswatch

from collections import OrderedDict

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

    # def test_uid(self):
    #     """
    #     Assert #uid returns a hashed representation of the instance.
    #     That representation comes from concatenation the keys of the
    #     instance's #to_odict method, and then running through a hashing
    #     algorithm.
    #     """
    #     uid = hash('#ffffffPNGRGB20x20')

    # def test_json_serialization(self):
    #     """
    #     Assert #to_json returns a well structured JSON representation.
    #     """
    #     i = autoswatch.Image()

    # def test_bytes(self):
    #     """
    #     Assert #bytes returns the image as a bytes string.
    #     """
    #     i = autoswatch.Image()
