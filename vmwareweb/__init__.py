import os
from flask import Flask
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


from vmwareweb.engines.view import engines_blueprints
from vmwareweb.engines.authentications import auth_blueprints
from vmwareweb.users.views import users

app.register_blueprint(engines_blueprints)
app.register_blueprint(auth_blueprints)
app.register_blueprint(users)
