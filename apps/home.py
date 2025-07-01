from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from model import Product # We don't need to import Review here directly for average_rating

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_authenticated and current_user.role == 'Farmer':
        return redirect('/dashboard')  # Only redirect farmers to dashboard
     # Get filter parameters from the query string
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    category = request.args.get('category')
    location = request.args.get('location')
    quantity_min = request.args.get('quantity_min', type=int)   
    quantity_max = request.args.get('quantity_max', type=int)   
    query = Product.query.filter_by(is_available=True)
    
    # Apply filters if provided
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)
    if category:
        query = query.filter(Product.category == category)
    if location:
        query = query.filter(Product.location == location)
    if quantity_min is not None:
        query = query.filter(Product.quantity >= quantity_min)
    if quantity_max is not None:
        query = query.filter(Product.quantity <= quantity_max)

    products = query.all()
    # Fetch all available products from the database
    # The 'average_rating' and 'total_reviews' properties will be accessible on each product object
    products = query.all()
    
    # Pass the actual Product objects to the template for full access
    return render_template('home.html', products=products)
