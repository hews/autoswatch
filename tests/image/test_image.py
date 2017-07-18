import unittest
import autoswatch

class ImageTest(unittest.TestCase):

    def test_defaults(self):
        """
        Assert that an Image is created with the defaults:
        a size of 20x20 in the form of a tuple, a default color string
        of the hex value #ffffff, a default color mode of 'RGB', and a
        default format of 'PNG'.
        """
        i = autoswatch.Image()
        self.assertEqual(i.size,   (20, 20))
        self.assertEqual(i.color,  '#ffffff')
        self.assertEqual(i.mode,   'RGB')
        self.assertEqual(i.format, 'PNG')

    # autoswatch.Image((40, 40), '#ff0000', 'RGBA', 'JPG')
    # autoswatch.Image(color='#ff0000')
    # i = autoswatch.Image(color='#ff0000')
    # (is JSON serializable via to_json)  i.to_json() is a dict like X
    # bytes() returns an immutable bytes string representation

if __name__ == '__main__':
    unittest.main()
