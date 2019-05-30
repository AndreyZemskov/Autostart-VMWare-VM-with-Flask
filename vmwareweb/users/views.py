""" users/view.py """

from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from vmwareweb import db
from vmwareweb.models import User
from vmwareweb.users.forms import LoginForm, ChangePasswordForm
from werkzeug.security import generate_password_hash

users = Blueprint('users', __name__)

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('users.adm'))
            return redirect(url_for('engines.index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('users.login'))

    return render_template("login.html", form=form)


@users.route("/logout", strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for("users.login"))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password_hash = generate_password_hash(form.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('engines.index'))
        else:
            flash('Invalid password.')
    return render_template("account.html", form=form)

@users.route("/admin", methods=['GET', 'POST'])
@login_required
def adm():
    return render_template('admin/index.html')

