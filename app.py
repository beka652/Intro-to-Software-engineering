from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'QWERTYUIOP'  
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) 
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(150), unique=True, nullable=False)
    city = db.Column(db.String(150), nullable=False)
    subcity = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def home():

    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register_authentication():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        city = request.form.get('city')
        subcity = request.form.get('subcity')
        role = request.form.get('role')

        if not all([username, password, email, phone, city, subcity, role]):
            return "All fields are required!", 400

        if User.query.filter_by(username=username).first():
            return "Username already exists!", 400
        if User.query.filter_by(email=email).first():
            return "Email already exists!", 400
        if User.query.filter_by(phone=phone).first():
            return "Phone number already exists!", 400

        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            phone=phone,
            city=city,
            subcity=subcity,
            role=role
        )
        db.session.add(new_user)
        db.session.commit() 

        return redirect(url_for('signin'))
    return render_template('register.html')
@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin_authentication():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Username and password are required!", 400

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user) # 

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

    return render_template('signin.html')

@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')

@app.route('/admin')
@login_required
def admin_page():
    if current_user.role != 'Admin':
        return "Access denied: Admins only!", 403 
    return render_template('admin.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
