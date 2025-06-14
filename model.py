from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'signin.signin'  # Use blueprint endpoint

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) 
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(150), unique=True, nullable=False)
    city = db.Column(db.String(150), nullable=False)
    subcity = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    id_picture = db.Column(db.String(200))  # Path or filename for ID picture
    face_picture = db.Column(db.String(200))  # Path or filename for face picture

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
