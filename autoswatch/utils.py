import re

from flask import render_template

HEX_COLOR_REGEX = r'^#(?:[0-9a-f]{3}){1,2}$'

def validate_hex_color(hex='#'):
    color = {}
    color['value'] = (hex if hex[0] == '#' else '#' + hex).lower()
    color['valid'] = bool(re.match(HEX_COLOR_REGEX, color['value']))
    return color

def register_routes(app, routes):
    app.register_blueprint(routes)

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.j2'), 404

    @app.errorhandler(400)
    def bad_request(error):
        return render_template('400.j2'), 400
