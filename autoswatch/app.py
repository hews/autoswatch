from flask import Flask, send_file

from autoswatch.image import Image

app = Flask(__name__)

app.config.from_object(__name__)
# app.config.from_envvar("AUTOSWATCH_SETTINGS", silent=True)

@app.route('/')
def root():
    return """
      <!doctype html>
      <html lang="en-US">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">

          <link rel="shortcut icon" href="/favicon.ico">

          <title>Autoswat.ch</title>

          <style>
            html {
              font-family: sans-serif;
              font-size: 20px;
              line-height: 1.4;
              text-align: center;
            }
            main {
              max-width: 600px;
              margin: 0 auto;
            }
          </style>
        </head>
        <body>
          <main>
            <h1>Welcome to Autoswat.ch!</h1>
            <p>
              <img src="http://localhost:5000/000" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
              <img src="http://localhost:5000/f00" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
              <img src="http://localhost:5000/0f0" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
              <img src="http://localhost:5000/00f" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
              <img src="http://localhost:5000/ff0" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
              <img src="http://localhost:5000/0ff" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
              <img src="http://localhost:5000/f0f" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
              <img src="http://localhost:5000/fff" width="20" height="20" style="border: 1px solid black; border-radius: 100%;">
            </p>
            <p>
              Please navigate to a link that represents a hex value color
              in order to generate a color swatch image on the fly.
              For example, try visiting: <br>
              <strong>
                <a href="http://localhost:5000/ff0000">https://autoswat.ch/ff0000</a>
              </strong>
            <p>
            <p>
              These are great for embedding into style guides, how-tos or
              example pages that are written in HTML, Markdown, etc.
            </p>
          </main>
        </body>
      </html>
    """

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

# TODO: handle favicon.ico requests correctly… Possibly:
#
# app.config['SERVER_NAME'] = 'localhost'
# with app.app_context():
#     app.add_url_rule('/favicon.ico',
#                  redirect_to=url_for('static', filename='favicon.ico'))
# @app.route('/favicon.ico')
# def favicon():
#     return send_file('./static/favicon.ico')

# TODO: create a fun home page that explains the project (and update
#   the README)

# TODO: check for values passed as query strings:
#   - size/s, in the format WIDTHxHEIGHT (in pixels); default 40x40
#   - filetype/ft, one of jpg, gif, png, or svg; default png
#   - text/t, some text to render on top of the image,
#   - text color/c, a color value for the text; default #fff
#   - requesttype/r (mirrors the HTTP header Request-Type), can
#     be xml, json or image, and sets the return type

