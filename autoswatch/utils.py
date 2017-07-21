import re

HEX_COLOR_REGEX = r'^#(?:[0-9a-f]{3}){1,2}$'

def validate_hex_color(hex='#'):
    color = {}
    color['value'] = (hex if hex[0] == '#' else '#' + hex).lower()
    color['valid'] = bool(re.match(HEX_COLOR_REGEX, color['value']))
    return color
