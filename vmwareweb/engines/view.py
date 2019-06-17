""" engines/view """

import re
from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required
from vmwareweb.engines.engine_threading import collection_start, monitoring_start, mail_start
from vmwareweb.engines.response_collections import collection_info, last_check_time
from vmwareweb.models import db, ServerList, MailSettings, RecipientsPost
from vmwareweb.engines.forms import ServerPost, EmailPost, RecipientsForm
from vmwareweb.engines.send_email import mail_test
from vmwareweb.engines.response_collections import mail_info
from vmwareweb import dinamic_mail_setting, mail, app


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


def prepare_mail():
    MailSettings.query.filter_by(id=1).delete()
    db.session.commit()
    return 0

@engines_blueprints.route('/mail_post', methods=['GET', 'POST'])
def mail_create():



    form = EmailPost()
    if form.validate_on_submit():
        prepare_mail()
        mail_post = MailSettings(mail_server=form.mail_server.data, username=form.username.data, password=form.password.data, protocol=form.protocol.data, port=form.port.data)
        db.session.add(mail_post)
        db.session.commit()
        dinamic_mail_setting()
        mail.init_app(app)

        return redirect(url_for('engines.mail_view'))

    return render_template('mail_post.html', form=form)


@engines_blueprints.route('/mail_panel', methods=['GET', 'POST'])
def mail_view():
    for email, usr, proto, ports in db.session.query(MailSettings.mail_server, MailSettings.username,
                                                     MailSettings.protocol, MailSettings.port):

        mail_server = re.search(r"[a-zA-Z]", str(email)).string
        mail_username = re.search(r"[a-zA-Z]", str(usr)).string
        protocol_view = re.search(r"[a-zA-Z]", str(proto)).string
        port_str = str(ports)
        mail_find = re.findall(r"^\d{1,3}", port_str)
        mail_port = mail_find[5:]


    return render_template('mail_panel.html', mail_server=mail_server, mail_username=mail_username, protocol_view=protocol_view, mail_port=mail_port, mail_info=mail_info)


@engines_blueprints.route('/recipients_post_mail', methods=['GET', 'POST'])
def recipients_email():

    form = RecipientsForm()
    if form.validate_on_submit():
        recipients_post = RecipientsPost(recipients=form.recipients.data)
        db.session.add(recipients_post)
        db.session.commit()
        flash('Recipient was added.', 'success')
        return redirect(url_for('engines.recipients_email'))

    return render_template('recipients.html', form=form)


@engines_blueprints.route('/send_test_mail')
def test_mail():
    mail_test()
    flash('Message was sended', 'test')
    return redirect(url_for('engines.mail_view'))


@engines_blueprints.route('/check_mail_srv')
def check_mail():
    mail_start()
    return redirect(url_for('engines.mail_view'))
