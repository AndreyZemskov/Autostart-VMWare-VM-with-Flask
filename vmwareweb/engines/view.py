""" engines/view """

from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required
from vmwareweb.engines.engine import collection_info, collection_start, monitoring_start, last_check_time
from vmwareweb.models import ServerList, db
from vmwareweb.engines.forms import ServerPost

engines_blueprints = Blueprint('engines', __name__)

@engines_blueprints.route('/srv_post', methods=['GET', 'POST'])
@login_required
def create_vm():
    form = ServerPost()
    if form.validate_on_submit():
        server_post = ServerList(vm_ip=form.vm_ip.data, hosts_ip=form.hosts_ip.data, esx_version=form.esx_version.data, vm_clone=form.vm_clone.data)
        db.session.add(server_post)
        db.session.commit()
        flash('Added')
        return redirect(url_for('engines.control_panel'))

    return render_template('vm_post.html', form=form)

@engines_blueprints.route('/')
def index():
    return render_template('index.html', collection_info=collection_info, last_check_time=last_check_time)

@engines_blueprints.route('/collection')
def view():
    collection_start()
    return redirect(url_for('engines.control_panel'))

@engines_blueprints.route('/monitoring_start')
def monitoring():
    monitoring_start()
    return redirect(url_for('engines.control_panel'))

@engines_blueprints.route('/control_panel')
@login_required
def control_panel():
    return render_template('control_panel.html', collection_info=collection_info, last_check_time=last_check_time)
