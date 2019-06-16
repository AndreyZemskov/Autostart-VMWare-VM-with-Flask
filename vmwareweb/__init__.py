import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin


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

from vmwareweb.settings_email import mail_server, mail_username, mail_port, mail_ssl, sd

app.config['MAIL_SERVER'] = mail_server
app.config['MAIL_PORT'] = mail_port
app.config['MAIL_USE_SSL'] = mail_ssl
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = sd
mail = Mail(app)


""" BLUEPRINTS SETUP """


from vmwareweb.engines.view import engines_blueprints
from vmwareweb.engines.authentications import auth_blueprints
from vmwareweb.users.views import users
from vmwareweb.engines.send_email import send_email_blueprints

app.register_blueprint(engines_blueprints)
app.register_blueprint(auth_blueprints)
app.register_blueprint(users)
app.register_blueprint(send_email_blueprints)