from fragforce import app
from flask import Blueprint, render_template, session, redirect, url_for, \
        request, abort
from flask_flatpages import FlatPages

mod = Blueprint('events', __name__, url_prefix='/events')
pages = FlatPages(app)

@mod.route('/')
def index(name=None):
  return render_template('events/index.html', name=name)

@mod.route('/live')
def live(name=None):
  return render_template('events/live.html', name=name)

@mod.route('/<path:path>/')
def page(path):
  page = pages.get_or_404('events/' + path)
  template = page.meta.get('template', 'flatpage.html')
  return render_template(template, page=page)
