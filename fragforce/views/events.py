from fragforce import app
from flask import Blueprint, render_template, session, redirect, url_for, \
        request, abort
from flask_flatpages import FlatPages
from random import sample
import os

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
  images = []
  if os.path.isdir(os.path.join(app.static_folder, 'images/events', path)):
    raw_images = os.listdir(os.path.join(app.static_folder, 'images/events', path))
    if len(raw_images) > 3:
      choices = sample(raw_images, 3)
    else:
      choices = raw_images
    for raw_image in choices:
      images.append(url_for('static', filename=os.path.join('images/events', path, raw_image)))
  template = page.meta.get('template', 'eventpage.html')
  return render_template(template, page=page, images=images)
