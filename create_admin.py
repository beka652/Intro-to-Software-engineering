from model import db, User
from werkzeug.security import generate_password_hash
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'QWERTYUIOP'
db.init_app(app)

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='Admin')
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()
        print('Admin user created.')
    else:
        print('Admin user already exists.')
    
    # ...existing code...
    if not User.query.filter_by(username='admin2').first():
        admin = User(username='admin2', email='admin2@example.com', role='Admin')
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()
        print('New admin user created.')
    else:
        print('Admin user already exists.')
