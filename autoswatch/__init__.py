import os

from flask import Flask

from autoswatch.routes import routes
from autoswatch.image  import Image

import autoswatch.utils as utils

def env_config(env=''):
    if 'test' in env:
        return {
            'DEBUG': False, # Should this be so?
            'TESTING': True
        }
    elif env == 'production':
        return {
            'DEBUG': False,
            'JSONIFY_PRETTYPRINT_REGULAR': False
        }
        # 'SEND_FILE_MAX_AGE_DEFAULT': seconds

    return {}

def create_app(configuration=None, instance_config_file='config.py'):
    app = Flask(
        __name__,
        static_url_path='',
        instance_relative_config=True
    )

    # Default configuration, then environment-bound default config,
    # and finally private, instance-based configuration loaded from
    # /instance/<instance_config_file> (if it exists).
    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY=b'>>>notsosecret<<<',
        JSON_AS_ASCII=False
    ))
    app.config.update(configuration or {})
    app.config.from_pyfile(instance_config_file, silent=True)

    utils.register_routes(app, routes)
    utils.register_error_handlers(app)

    return app

# AND HERE WE REGISTER A DEFAULT APP TO EXPOSE TO OUR APP SERVER.
app = create_app(env_config(os.environ['ENV']))


# ######################################################################
# TODO: cache the image according to a unique id, and send with long-
#   lived cache instructions.
#
#   Cache-Control: public, max-age=31536000
#
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

