""" engines/forms """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from vmwareweb.engines.engine import esx_list

class ServerPost(FlaskForm):
    vm_ip = StringField('Virtual Machine')
    hosts_ip = StringField('Host IP')
    esx_version = SelectField('ESX Version', choices=esx_list)
    vm_clone = StringField('VM Clone')
    submit = SubmitField("Post")