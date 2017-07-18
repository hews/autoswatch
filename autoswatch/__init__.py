# from autoswatch.image_generator import ImageGenerator

from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar("AUTOSWATCH_SETTINGS", silent=True)

@app.route("/")
def root():
    return ">> Swatch, AH-ahh!\n"

@app.route("/about")
def about():
    return ">> Get some swatches, bruzette."

@app.route("/instructions")
def instructions():
    return ">> Here's how to use it, bozo."

@app.route("/<value>")
def valueOnly(value):
    return "The hex value is #%s\n" % (value)

@app.route("/<format>/<value>")
def formatAndValue(format, value):
    return "The %s value is #%s\n" % (format, value)

@app.route("/<value>/size/<size>")
def valueOnlyWithSize(value, size): pass

@app.route("/<format>/<value>/size/<size>")
def formatAndValueWithSize(format, value, size): pass

# also check for an &filetype=svg, or a requesttype

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
