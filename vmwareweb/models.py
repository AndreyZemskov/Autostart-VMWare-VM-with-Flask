from vmwareweb import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from vmwareweb import admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort
from cryptography.fernet import Fernet
from simplecrypt import encrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Username {}".format(self.username)



class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)

    def not_auth(self):
        return "You are not auth"


class ServerList(db.Model):

    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    vm_ip = db.Column(db.String(15), unique=True, index=True) # VM for listening
    hosts_ip = db.Column(db.String(15), index=True) # Hosts where is located cope VM
    esx_version = db.Column(db.String(15), index=True)
    vm_clone = db.Column(db.String(15), unique=True, index=True)


    def __init__(self, vm_ip,hosts_ip, esx_version, vm_clone):
        self.vm_ip = vm_ip
        self.hosts_ip = hosts_ip
        self.esx_version = esx_version
        self.vm_clone = vm_clone


    def __repr__(self):
        return "{} {} {} {}".format(self.vm_ip, self.hosts_ip, self.esx_version, self.vm_clone)


key = Fernet.generate_key()

f = Fernet(key)


class MailSettings(db.Model):

    __tablename__ = 'email_settings'

    id = db.Column(db.Integer, primary_key=True)
    mail_server = db.Column(db.String(30), index=True)
    username = db.Column(db.String(15), unique=True, index=True) # VM for listening
    password = db.Column(db.String(200), index=True) # Hosts where is located cope VM
    protocol = db.Column(db.String(15), index=True)
    port = db.Column(db.SmallInteger, index=True)


    def __init__(self, mail_server, username, password, protocol, port):
        self.mail_server = mail_server
        self.username = username
        self.password = bytes(encrypt('password', password))
        self.protocol = protocol
        self.port = port

    def __repr__(self):
        return "{} {} {} {} {}".format(self.mail_server, self.username, self.password, self.protocol, self.port)


class RecipientsPost(db.Model):

    __tablename__ = 'recipients'

    id = db.Column(db.Integer, primary_key=True)
    recipients = db.Column(db.String(50), index=True)


    def __init__(self, recipients):
        self.recipients = recipients

    def __repr__(self):
        return "{}".format(self.recipients)


admin.add_view(Controller(ServerList, db.session))
admin.add_view(Controller(RecipientsPost, db.session))