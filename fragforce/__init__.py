from flask import Flask
app = Flask(__name__)

app.config.from_object('config')

from fragforce.views import general
from fragforce.views import events

app.register_blueprint(general.mod)
app.register_blueprint(events.mod)
