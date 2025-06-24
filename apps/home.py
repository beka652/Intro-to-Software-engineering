from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from model import Product # We don't need to import Review here directly for average_rating

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_authenticated and current_user.role == 'Farmer':
        return redirect('/dashboard')  # Only redirect farmers to dashboard
    
    # Fetch all available products from the database
    # The 'average_rating' and 'total_reviews' properties will be accessible on each product object
    products = Product.query.filter_by(is_available=True).all()
    
    # Pass the actual Product objects to the template for full access
    return render_template('home.html', products=products)
