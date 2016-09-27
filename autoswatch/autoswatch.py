
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def root():
    return "Swatch, AH-ah!"

app.config.from_envvar("AUTOSWATCH_SETTINGS", silent=True)

