from flask import Blueprint, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from model import User, db
from flask_login import login_user

register_bp = Blueprint('register', __name__)
UPLOAD_FOLDER = 'static/uploads'

@register_bp.route('/', methods=['GET'])
def register():
    return render_template('register.html')

@register_bp.route('/submit', methods=['POST'])
def register_authentication():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    role = request.form.get('userRole')
    # Farmer fields
    phone = request.form.get('phoneNumber')
    city = request.form.get('city')
    subcity = request.form.get('subCity')
    # Create user folder by email
    user_folder = os.path.join(UPLOAD_FOLDER, email)
    os.makedirs(user_folder, exist_ok=True)
    id_picture = None
    face_picture = None

    if role == 'farmer':
        id_picture_file = request.files.get('idPicture')
        face_picture_file = request.files.get('facePicture')
        if id_picture_file and id_picture_file.filename:
            id_picture = secure_filename(id_picture_file.filename)
            id_picture_path = os.path.join(user_folder, id_picture)
            id_picture_file.save(id_picture_path)
            id_picture = os.path.join(email, id_picture)  # store relative path
        if face_picture_file and face_picture_file.filename:
            face_picture = secure_filename(face_picture_file.filename)
            face_picture_path = os.path.join(user_folder, face_picture)
            face_picture_file.save(face_picture_path)
            face_picture = os.path.join(email, face_picture)  # store relative path
    # Validation
    if role == 'farmer':
        if not all([username, password, email, phone, city, subcity, id_picture, face_picture]):
            return "All fields are required for farmers!", 400
    else:
        if not all([username, password, email, role]):
            return "All fields are required!", 400

    if User.query.filter_by(username=username).first():
        return "Username already exists!", 400
    if User.query.filter_by(email=email).first():
        return "Email already exists!", 400
    if role == 'farmer' and User.query.filter_by(phone=phone).first():
        return "Phone number already exists!", 400

    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        phone=phone if role == 'farmer' else '',
        city=city if role == 'farmer' else '',
        subcity=subcity if role == 'farmer' else '',
        role=role,
        id_picture=id_picture,
        face_picture=face_picture
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    return redirect(url_for('home.home'))