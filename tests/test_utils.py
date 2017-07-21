from autoswatch.utils import validate_hex_color

from nose.tools import assert_equals, assert_true, assert_false

class TestUtils:

    def test_val_hex_defaults_to_false(self):
        """
        Assert that validate_hex_color returns false by default.
        """
        info = validate_hex_color()
        assert_false(info['valid'])

    def test_val_hex_true_when_hex_color(self):
        """
        Assert that validate_hex_color returns true when valid hex color.
        """
        assert_true(validate_hex_color('000000')['valid'])
        assert_true(validate_hex_color('ffffff')['valid'])
        assert_true(validate_hex_color('aaa')['valid'])
        assert_true(validate_hex_color('111')['valid'])
        assert_true(validate_hex_color('FeeDad')['valid'])
        assert_true(validate_hex_color('0A0')['valid'])

    def test_val_hex_false_when_not_hex_color(self):
        """
        Assert that validate_hex_color returns false when not a valid hex color.
        """
        assert_false(validate_hex_color('0')['valid'])
        assert_false(validate_hex_color('fffffff')['valid'])
        assert_false(validate_hex_color('aaaa')['valid'])
        assert_false(validate_hex_color('11G')['valid'])
        assert_false(validate_hex_color('NOT')['valid'])

    def test_val_hex_true_when_with_octothorpe(self):
        """
        Assert that validate_hex_color returns true when includes octothorpe.
        Of course, this assumes that the hex is valid.
        """
        assert_true(validate_hex_color('#ff0000')['valid'])
        assert_true(validate_hex_color('#111')['valid'])
        assert_false(validate_hex_color('#aaaa')['valid'])

    def test_val_hex_true_returns_formatted_value(self):
        """
        Assert that validate_hex_color returns a formatted value.
        A formatted value includes a beginning octothorpe and has all
        letters in lowercase.
        """
        assert_equals(validate_hex_color('AB0011')['value'], '#ab0011')

