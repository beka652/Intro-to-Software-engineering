from flask import Blueprint, redirect, render_template, request, url_for, flash, jsonify
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
    # Get form data
    form_data = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'email': request.form.get('email'),
        'role': request.form.get('userRole'),
        'phone': request.form.get('phoneNumber'),
        'city': request.form.get('city'),
        'subcity': request.form.get('subCity')
    }
    
    # Basic validation
    if not form_data['username'] or not form_data['password'] or not form_data['email'] or not form_data['role']:
        flash('Please fill in all required fields', 'danger')
        return render_template('register.html', form_data=form_data)
    
    # Check if username or email already exists
    if User.query.filter_by(username=form_data['username']).first():
        flash('Username already exists!', 'danger')
        return render_template('register.html', form_data=form_data)
    if User.query.filter_by(email=form_data['email']).first():
        flash('Email already exists!', 'danger')
        return render_template('register.html', form_data=form_data)

    # Handle farmer-specific fields
    if form_data['role'] == 'Farmer':
        # Validate farmer fields
        if not all([form_data['phone'], form_data['city'], form_data['subcity']]):
            flash('Please fill in all farmer information fields', 'danger')
            return render_template('register.html', form_data=form_data)
        
        id_picture_file = request.files.get('idPicture')
        face_picture_file = request.files.get('facePicture')
        
        if not id_picture_file or not face_picture_file:
            flash('Please upload both ID and face pictures', 'danger')
            return render_template('register.html', form_data=form_data)

        # Check if phone number exists
        if User.query.filter_by(phone=form_data['phone']).first():
            flash('Phone number already exists!', 'danger')
            return render_template('register.html', form_data=form_data)

        # Create user folder and save pictures
        user_folder = os.path.join(UPLOAD_FOLDER, form_data['email'])
        os.makedirs(user_folder, exist_ok=True)

        # Save ID picture
        id_picture = secure_filename(id_picture_file.filename)
        id_picture_path = os.path.join(user_folder, id_picture)
        id_picture_file.save(id_picture_path)
        id_picture = os.path.join(form_data['email'], id_picture)

        # Save face picture
        face_picture = secure_filename(face_picture_file.filename)
        face_picture_path = os.path.join(user_folder, face_picture)
        face_picture_file.save(face_picture_path)
        face_picture = os.path.join(form_data['email'], face_picture)

        # Create farmer user
        new_user = User(
            username=form_data['username'],
            email=form_data['email'],
            password_hash=generate_password_hash(form_data['password'], method='pbkdf2:sha256'),
            phone=form_data['phone'],
            city=form_data['city'],
            subcity=form_data['subcity'],
            role=form_data['role'],
            id_picture=id_picture,
            face_picture=face_picture
        )
    else:
        # Create buyer user
        new_user = User(
            username=form_data['username'],
            email=form_data['email'],
            password_hash=generate_password_hash(form_data['password'], method='pbkdf2:sha256'),
            role=form_data['role']
        )

    try:
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Registration successful!', 'success')
        
        # Redirect based on role
        if form_data['role'] == 'Farmer':
            return redirect(url_for('dashboard.dashboard'))
        else:
            return redirect(url_for('home.home'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during registration. Please try again.', 'danger')
        return render_template('register.html', form_data=form_data)