from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy() # Assuming db is initialized elsewhere (e.g., app.py) and imported here
login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False) # e.g., 'Customer', 'Farmer', 'Admin'
    
    # Farmer specific fields (can be nullable for customers)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    subcity = db.Column(db.String(50), nullable=True)
    id_picture = db.Column(db.String(255), nullable=True) # Path to ID picture
    face_picture = db.Column(db.String(255), nullable=True) # Path to face picture

    # Relationships
    products = db.relationship('Product', backref='farmer', lazy=True)
    reviews_given = db.relationship('Review', backref='reviewer', lazy=True) # Reviews given by this user
    replies_given = db.relationship('Reply', backref='farmer', lazy=True) # Replies given by this user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=True)  # e.g., 'Kg', 'Unit', 'Litre'
    image_path = db.Column(db.String(255), nullable=True) # Path to product image
    is_available = db.Column(db.Boolean, default=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # New relationship for reviews
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')

    @property
    def average_rating(self):
        """Calculates the average rating for the product based on its reviews."""
        if not self.reviews:
            return 0.0 # Return 0 if no reviews
        total_rating = sum(review.rating for review in self.reviews)
        return round(total_rating / len(self.reviews), 1) # Round to one decimal place

    @property
    def total_reviews(self):
        """Returns the total number of reviews for the product."""
        return len(self.reviews)

    def __repr__(self):
        return f'<Product {self.name}>'

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # Star rating (e.g., 1 to 5)
    comment = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship to fetch farmer replies to this review
    replies = db.relationship('Reply', backref='review', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Review Product:{self.product_id} User:{self.user_id} Rating:{self.rating}>'

class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reply_text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reply Review:{self.review_id} Farmer:{self.farmer_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

