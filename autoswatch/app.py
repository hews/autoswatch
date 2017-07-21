from flask import Flask, send_file, render_template, abort

from autoswatch.image import Image
from autoswatch.utils import validate_hex_color

app = Flask(__name__, static_url_path='')

app.config.from_object(__name__)
app.config.from_envvar("CONFIG_FILE", silent=True)

@app.route('/')
def root():
    return render_template('index.j2')

@app.route('/hex/<hex_color>')
def value_only(hex_color):
    color = validate_hex_color(hex_color)
    if not color['valid']:
        return abort(400)

    buffer = Image(color=color['value']).byte_stream()
    return send_file(buffer, mimetype='image/png')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.j2'), 404

@app.errorhandler(400)
def bad_request(error):
    return render_template('400.j2'), 400

# TODO: generate when given a variety of types of hex value
#   test:
#   - with or without octothorpe (%23)
#   - upper or lowercase
#   - three-letter
#   - html known colors

# TODO: cache the image according to a unique id
#   From https://stackoverflow.com/a/15226368:
#
#   import redis
#
#   i = Image.new(…)
#   r = redis.StrictRedis(host='localhost')
#   r.set(i.guid(), i.bytes())
#
#   …
#
#   b = r.get(i.guid())

# TODO: be able to return a json payload with a link to the image
#   (and when the original request is made, we cache an image there)

# TODO: also work for RGB(A), HSV and CMYK
#
#   @app.route("/<format>/<value>")
#   def format_and_value(format, value):
#       return "The %s value is #%s\n" % (format, value)

# TODO: create a fun home page that explains the project (and update
#   the README)

# TODO: check for values passed as query strings:
#   - size/s, in the format WIDTHxHEIGHT (in pixels); default 40x40
#   - filetype/ft, one of jpg, gif, png, or svg; default png
#   - text/t, some text to render on top of the image,
#   - text color/c, a color value for the text; default #fff
#   - requesttype/r (mirrors the HTTP header Request-Type), can
#     be xml, json or image, and sets the return type

