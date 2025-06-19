from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from model import User

signin_bp = Blueprint('signin', __name__)

@signin_bp.route('/')
def signin():
    return render_template('signin.html')

@signin_bp.route('/', methods=['POST'])
def signin_authentication():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username and password are required!', 'danger')
        return redirect(url_for('signin.signin'))

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        flash(f'Welcome back, {username}!', 'success')

        # Normalize role to title case for redirect logic
        role = user.role.title() if user.role else ''
        if role == 'Farmer':
            return redirect(url_for('dashboard.dashboard'))  # Redirect farmers to dashboard
        else:
            return redirect(url_for('home.home'))  # Redirect buyers to home page
    else:
        flash('Invalid username or password!', 'danger')
        return redirect(url_for('signin.signin'))