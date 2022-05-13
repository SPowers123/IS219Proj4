from werkzeug.security import generate_password_hash
from app.auth.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from app.db import db
from app.db.models import User
from app.auth.decorators import admin_required


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    loginform = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('recipes.my_recipes'))
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user is None or not user.check_password(loginform.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Welcome!', 'success')
            return redirect(url_for('recipes.my_recipes'))
    return render_template('login.html', form=loginform)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    registerform = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('recipes.my_recipes'))
    if registerform.validate_on_submit():
        user = User.query.filter_by(email=registerform.email.data).first()
        if user is None:
            user = User(email=registerform.email.data, password=generate_password_hash(registerform.password.data))
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()
            flash('Thank you for registering!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('This email is already registered.')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=registerform)


@auth.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/users')
@login_required
@admin_required
def browse_users():
    data = User.query.all()
    titles = [('email', 'Email'), ('registered_on', 'Registered On')]
    retrieve_url = ('auth.retrieve_user', [('user_id', ':id')])
    edit_url = ('auth.edit_user', [('user_id', ':id')])
    add_url = url_for('auth.add_user')
    delete_url = ('auth.delete_user', [('user_id', ':id')])

    current_app.logger.info("Browse page loading")

    return render_template('browse.html', titles=titles, add_url=add_url, edit_url=edit_url, delete_url=delete_url,
                           retrieve_url=retrieve_url, data=data, User=User, record_type="Users")


@auth.route('/users/<int:user_id>')
@login_required
def retrieve_user(user_id):
    user = User.query.get(user_id)
    return render_template('profile_view.html', user=user)


@auth.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    editform = UserEditForm(obj=user)
    if editform.validate_on_submit():
        user.about = editform.about.data
        user.is_admin = int(editform.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash('User Edited Successfully', 'success')
        current_app.logger.info("edited a user")
        return redirect(url_for('auth.browse_users'))
    return render_template('user_edit.html', form=editform)


@auth.route('/users/new', methods=['POST', 'GET'])
@login_required
def add_user():
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        user = User.query.filter_by(email=registerform.email.data).first()
        if user is None:
            user = User(email=registerform.email.data, password=generate_password_hash(registerform.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you just created a user', 'success')
            return redirect(url_for('auth.browse_users'))
        else:
            flash('Already Registered')
            return redirect(url_for('auth.browse_users'))
    return render_template('user_new.html', form=registerform)


@auth.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user.id == current_user.id:
        flash("You can't delete yourself!")
        return redirect(url_for('auth.browse_users'), 302)
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted', 'success')
    return redirect(url_for('auth.browse_users'), 302)


@auth.route('/profile', methods=['POST', 'GET'])
def edit_profile():
    user = User.query.get(current_user.get_id())
    profileform = ProfileForm(obj=user)
    if profileform.validate_on_submit():
        user.about = profileform.about.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Profile', 'success')
        return render_template('profile_view.html', user=user)
    return render_template('profile_edit.html', form=profileform)


@auth.route('/account', methods=['POST', 'GET'])
def edit_account():
    user = User.query.get(current_user.get_id())
    securityform = RegisterForm(obj=user)
    if securityform.validate_on_submit():
        user.email = securityform.email.data
        user.password = securityform.password.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Password or Email', 'success')
        return render_template('profile_view.html', user=user)
    return render_template('manage_account.html', form=securityform)


