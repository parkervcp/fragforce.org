from flask import Flask
app = Flask(__name__)

app.config.from_object('config')

from fragforce.views import general

app.register_blueprint(general.mod)
