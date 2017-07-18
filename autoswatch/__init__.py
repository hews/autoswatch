from flask import Flask

from autoswatch.image import Image #, ImageGenerator

app = Flask(__name__)

app.config.from_object(__name__)
# app.config.from_envvar("AUTOSWATCH_SETTINGS", silent=True)

@app.route("/")
def root():
    return ">> Swatch, AH-ahh!\n"

@app.route("/<value>")
def valueOnly(value):
    return "The hex value is #%s\n" % (value)

# TODO: generate simple pngs

# TODO: generate when given a variety of types of hex value

# TODO: generate unique ids from canonicalized json representations of
#   images that have been hashed.
#   See: https://stackoverflow.com/a/4670638.

# TODO: cache the image according to a unique id
#   From https://stackoverflow.com/a/15226368:
#
#   import PIL
#   import redis
#   import io
#
#   i = PIL.Image.new(…)
#   r = redis.StrictRedis(host='localhost')
#
#   with io.BytesIO() as byte_stream:
#      i.save(byte_stream, format='…')
#      r.set('imagedata', byte_stream.getvalue())
#
#   …
#
#   redis-cli --raw get 'imagedata' > test.png

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

