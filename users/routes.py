from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
#from mysite import db, bcrypt
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from mysite.models.models import User
from flask_login import login_user, current_user, logout_user, login_required
from .utils import send_reset_email, save_picture

users = Blueprint('users',__name__)

@users.route("/users/reset_password/<token>", methods=['POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user in None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    return render_template('users/reset_token.html', title = '', form=form)



@users.route("/users/reset_password", methods=['POST'])
def reset_request(post_id):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filer_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html',title='Reset Password',form=form)

@users.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
#        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#        db.session.add(user)
#        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
 #       if user and bcrypt.check_password_hash(user.password, form.password.data):
 #           login_user(user, remember=form.remember.data)
 #           next_page = request.args.get('next')
 #           return redirect(next_page) if next_page else redirect(url_for('main.index'))
 #       else:
 #           flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            flash('Picture Changed','info')
        current_user.username = form.username.data
        current_user.email = form.email.data
#        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template('users/account.html', title='Account', image_file = image_file, form = form)