import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

Bootstrap(app)


""" DATABASE SETUP """

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'datasqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
admin = Admin(app)

""" LOGIN CONFIGS """

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


""" EMAIL SETUP """

from vmwareweb.models import MailSettings, db
from simplecrypt import decrypt


def dinamic_mail_setting():
    mail = db.session.query(MailSettings.mail_server)
    username = db.session.query(MailSettings.username)
    password = db.session.query(MailSettings.password)
    protocol = db.session.query(MailSettings.protocol)
    port = db.session.query(MailSettings.port)

    mail_server = (str(mail[0]).replace("('", "").replace("',)", ""))
    mail_port = int(str(port[0]).replace("(", "").replace(",)", ""))
    mail_ssl = bool(str(protocol[0]).replace("('", "").replace("',)", ""))
    mail_username = (str(username[0]).replace("('", "").replace("',)", ""))
    mail_password = password[0]

    pas = mail_password[0]
    sd = str(decrypt('password', pas)).replace("b'", "").replace("'", "")

    app.config['MAIL_SERVER'] = mail_server
    app.config['MAIL_PORT'] = mail_port
    app.config['MAIL_USE_SSL'] = mail_ssl
    app.config['MAIL_USERNAME'] = mail_username
    app.config['MAIL_PASSWORD'] = sd

dinamic_mail_setting()
mail = Mail(app)


""" LOGGER SETUP """

logging.basicConfig(filename="application.log", level=logging.INFO)


""" BLUEPRINTS SETUP """


from vmwareweb.engines.view import engines_blueprints
from vmwareweb.engines.authentications import auth_blueprints
from vmwareweb.users.views import users
from vmwareweb.engines.send_email import send_email_blueprints

app.register_blueprint(engines_blueprints)
app.register_blueprint(auth_blueprints)
app.register_blueprint(users)
app.register_blueprint(send_email_blueprints)
