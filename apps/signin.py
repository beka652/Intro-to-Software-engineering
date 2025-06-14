from flask import Blueprint, redirect, render_template, request, url_for
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
        return "Username and password are required!", 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)

        if user.role == 'Farmer':
            return redirect(url_for('dashboard'))
        elif user.role == 'Customer':
            return redirect(url_for('home'))
        elif user.role == 'Admin':
            return redirect(url_for('admin_page'))
        else:
            return redirect(url_for('home'))
    else:
        return "Invalid username or password!", 401