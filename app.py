from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'QWERTYUIOP'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(150), unique=True, nullable=False)
    city= db.Column(db.String(150), nullable=False)
    subcity = db.Column(db.String(150), nullable=False)  # Remove unique=True if not needed

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    phone = request.form.get('phone')
    city = request.form.get('city')
    subcity = request.form.get('subcity')

    # Validate input
    if not username or not password:
        return "Username and password are required!", 400

    # Check if username exists
    if User.query.filter_by(username=username).first():
        return "Username already exists!", 400

    # Hash password and store user
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password=password_hash, email=email, phone=phone, city=city, subcity=subcity)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)