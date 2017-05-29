from fragforce import app
from flask import Blueprint, render_template, session, redirect, url_for, \
    request, abort
from flask_flatpages import FlatPages, pygments_style_defs

mod = Blueprint('general', __name__)


@mod.route('/')
def index(name=None):
    return render_template('general/index.html', name=name)


@mod.route('/contact')
def contact(name=None):
    return render_template('general/contact.html', name=name)


@mod.route('/donate')
def donate(name=None):
    return render_template('general/donate.html', name=name)


@mod.route('/join')
def join(name=None):
    return render_template('general/join.html', name=name)


@mod.route('/tracker')
def tracker(name=None):
    return render_template('tracker.html', name=name)


@mod.route('/static/css/pygments.css')
def pygments_css():
    return pygments_style_defs(), 200, {'Content-Type': 'text/css'}

@mod.route('/firewalls/aliases/<string:section>/<int:year>/')
def section_archives_year(section, year):
    if not section_exists(section):
        abort(404)
    templates = []
    templates.append('%s/archives.html' % section)
    templates.append('default_templates/archives.html')
    years = get_years(get_pages(pages, section=section))
    things = get_pages(pages, section=section, year=year)
    return render_template(templates, pages=things, section=section, years=years, year=year)
