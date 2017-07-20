from flask import Flask, send_file

import io

from autoswatch.image import Image

app = Flask(__name__)

app.config.from_object(__name__)
# app.config.from_envvar("AUTOSWATCH_SETTINGS", silent=True)

# app.config['SERVER_NAME'] = 'localhost'
# with app.app_context():
#     app.add_url_rule('/favicon.ico',
#                  redirect_to=url_for('static', filename='favicon.ico'))
# @app.route('/favicon.ico')
# def favicon():
#     return send_file('./static/favicon.ico')

@app.route('/')
def root():
    return ">> Swatch, AH-ahh!\n"

@app.route('/<value>')
def valueOnly(value):
    buffer = Image(color='#' + value).byte_stream()
    return send_file(buffer, mimetype='image/png')

# TODO: generate when given a variety of types of hex value
#   test:
#   - with or without octothorpe (%23)
#   - upper or lowercase
#   - three-letter
#   - html known colors

# TODO: generate unique ids from canonicalized json representations of
#   images that have been hashed.
#   See: https://stackoverflow.com/a/4670638.

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
#   def formatAndValue(format, value):
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

