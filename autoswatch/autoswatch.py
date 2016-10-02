
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar("AUTOSWATCH_SETTINGS", silent=True)

@app.route("/")
def root():
    return ">> Swatch, AH-ah!"

@app.route("/about")
def about():
    return ">> Get some swatches, bruzette."

@app.route("/instructions")
def instructions():
    return ">> Here's how to use it, bozo."

@app.route("/<value>")
def valueOnly(value):
    return ""

@app.route("/<format>/<value>")
def formatAndValue(format, value):
    return "The %s value is #%s" % (format, value)

@app.route("/<value>/size/<size>")
def valueOnlyWithSize(value, size): pass

@app.route("/<format>/<value>/size/<size>")
def formatAndValueWithSize(format, value, size): pass

# also check for an &filetype=svg, or a requesttype

