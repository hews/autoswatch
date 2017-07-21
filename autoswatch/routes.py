from flask import (
    Flask,
    Blueprint,
    send_file,
    render_template,
    abort
)

from autoswatch.image import Image
from autoswatch.utils import validate_hex_color

routes = Blueprint('autoswatch', __name__)

@routes.route('/')
def root():
    return render_template('index.j2')

@routes.route('/hex/<hex_color>')
def value_only(hex_color):
    color = validate_hex_color(hex_color)
    if not color['valid']:
        return abort(400)

    buffer = Image(color=color['value']).byte_stream()
    return send_file(buffer, mimetype='image/png')

