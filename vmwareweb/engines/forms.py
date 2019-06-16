""" engines/forms """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from vmwareweb.engines.engine import esx_list, protocol_list

class ServerPost(FlaskForm):
    vm_ip = StringField('Virtual Machine', validators=[DataRequired()])
    hosts_ip = StringField('Host IP', validators=[DataRequired()])
    esx_version = SelectField('ESX Version', choices=esx_list)
    vm_clone = StringField('VM Clone', validators=[DataRequired()])
    submit = SubmitField("Post")


class EmailPost(FlaskForm):
    mail_server = StringField('SMTP Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    protocol = SelectField('Protocol', choices=protocol_list)
    port = StringField('Port', validators=[DataRequired()])
    submit = SubmitField("Post")


class RecipientsForm(FlaskForm):
    recipients = StringField('Secipients', validators=[DataRequired()])
    submit = SubmitField("Post")