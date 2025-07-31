from model import db, login_manager
from apps.register import register_bp
from apps.signin import signin_bp
from apps.home import home_bp
from apps.dashboard import dashboard_bp
from apps.admin import admin_bp
from apps.products import products_bp
from apps.cart import cart_bp
from flask import Flask, render_template
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'QWERTYUIOP'
db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/feedback',methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST' :
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        user_type = request.form['user_type']
        
        new_feedback = Feedback(name=name, email=email, message=message, user_id=user_type)
        try:
            db.session.add(new_feedback)
            db.session.commit()
            flash('Thank you for your feedback!', 'success')
        except:
            flash('Error submitting feedback. Please try again.', 'danger')
        
    return rendet_template('feedback.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(signin_bp, url_prefix='/signin')
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(cart_bp, url_prefix='/cart')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)