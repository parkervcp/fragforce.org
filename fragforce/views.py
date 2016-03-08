from fragforce import app
from flask import render_template

@app.route('/')
def index(name=None):
  return render_template('index.html', name=name)
@app.route('/contact')
def contact(name=None):
  return render_template('contact.html', name=name)
@app.route('/join')
def join(name=None):
  return render_template('join.html', name=name)
