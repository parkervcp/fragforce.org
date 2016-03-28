from fragforce import app
from flask import Blueprint, render_template, session, redirect, url_for, \
        request, abort

mod = Blueprint('general', __name__, url_prefix='/events')

@mod.route('/')
def index(name=None):
  return render_template('events/index.html', name=name)
