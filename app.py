import os
from flask import Flask, render_template
from model import db, login_manager
from apps.register import register_bp
from apps.signin import signin_bp
from apps.home import home_bp
from apps.dashboard import dashboard_bp
from apps.admin import admin_bp
from apps.products import products_bp

app = Flask(__name__)

# Store the database in the instance folder
db_path = os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SECRET_KEY'] = 'QWERTYUIOP'
db.init_app(app)
login_manager.init_app(app)

@app.route('/')
def welcome():
    return render_template('welcome.html')

app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(signin_bp, url_prefix='/signin')
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(products_bp, url_prefix='/products')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
