from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'signin.signin'  # Use blueprint endpoint

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) 
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(150), unique=True, nullable=True)  # Now nullable
    city = db.Column(db.String(150), nullable=True)  # Now nullable
    subcity = db.Column(db.String(150), nullable=True)  # Now nullable
    role = db.Column(db.String(20), nullable=False)
    id_picture = db.Column(db.String(200))  # Path or filename for ID picture
    face_picture = db.Column(db.String(200))  # Path or filename for face picture

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    # --- NEW: Added 'unit' column ---
    unit = db.Column(db.String(20), nullable=False, default='unit') # Stores 'unit' or 'kilogram'
    image_path = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    farmer = db.relationship('User', backref=db.backref('products', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
