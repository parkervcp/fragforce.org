from fragforce import app
from flask import Blueprint, render_template, session, redirect, url_for, \
    request, abort
from flask_flatpages import FlatPages, pygments_style_defs
import re
import os

mod = Blueprint('general', __name__)
RE_FW_TABLE_NAME = re.compile(r'^[a-zA-Z0-9]+\.(nets|ports|urls|ips)$')
FW_ALIAS_PATH_FIXER = re.compile(r'^(https://.*/)firewalls/aliases.*')


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


@mod.route('/firewalls/tables/<string:table_type>/<string:folder>/<string:fname>')
def firewall_tables_nets(table_type, folder, fname):
    if table_type not in ['ports', 'nets']:
        abort(404)
    # if fname not in os.listdir(os.path.join(app.instance_path, app.template_folder, 'fwaliases', table_type)):
    #     abort(404)
    if not RE_FW_TABLE_NAME.match(fname):
        abort(404)

    return render_template('fwaliases/%s/%s/%s' % (table_type, folder, fname), table_type=table_type, base_name=fname,
                           folder=folder)


@mod.route('/firewalls/tables/<string:table_type>/<string:fname>')
def firewall_tables_ports(table_type, fname):
    if table_type not in ['ports', 'nets']:
        abort(404)
    # if fname not in os.listdir(os.path.join(app.instance_path, app.template_folder, 'fwaliases', table_type)):
    #     abort(404)
    if not RE_FW_TABLE_NAME.match(fname):
        abort(404)

    return render_template('fwaliases/%s/%s' % (table_type, fname), table_type=table_type, base_name=fname)


@mod.route('/firewalls/aliases/backup.xml')
def alias_backup_gen():
    """ Return an XML doc that can be restored via the pfsense backup interface. It will load all aliases. """
    from fragforce.pfsense import AliasBackup
    import os, os.path
    import urllib

    root_url = FW_ALIAS_PATH_FIXER.match(request.base_url).groups()[0]

    port_path = os.path.join(app.config['BASE_DIR'], 'fragforce', 'templates', 'fwaliases', 'ports')
    nets_path = os.path.join(app.config['BASE_DIR'], 'fragforce', 'templates', 'fwaliases', 'nets')

    ab = AliasBackup()

    def visit_port(aba, dirname, names):
        for file_name in names:
            path = os.path.join(dirname, file_name)
            if file_name.endswith('.ports'):
                url = root_url + "/firewalls/tables/ports/" + file_name
                ab.add_port_alias(name=file_name.replace('.ports', ''), url=url, update_frequency_days=1,
                                  description="Port Table %r" % file_name)

    def visit_nets(aba, dirname, names):
        for file_name in names:
            path = os.path.join(dirname, file_name)
            folder = os.path.split(dirname)[-1]
            if file_name.endswith('.nets'):
                url = root_url + "/firewalls/tables/nets/%s/%s" % (folder, file_name)
                ab.add_ip_alias(name=file_name.replace('.nets', ''), url=url, update_frequency_days=1,
                                description='Network Table %r' % file_name)
            elif file_name.endswith('.ips'):
                url = root_url + "/firewalls/tables/nets/%s/%s" % (folder, file_name)
                ab.add_ip_alias(name=file_name.replace('.ips', ''), url=url, update_frequency_days=1,
                                description='IP Table %r' % file_name)

    os.path.walk(port_path, visit_port, ab)
    os.path.walk(nets_path, visit_nets, ab)

    return ab.render(pretty=False)
