from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from model import Product # We don't need to import Review here directly for average_rating

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_authenticated and current_user.role == 'Farmer':
        return redirect('/dashboard')  # Only redirect farmers to dashboard
    search_query = request.args.get('search', '').strip()
    if search_query:
        products = Product.query.filter(Product.is_available == True, Product.name.ilike(f"%{search_query}%")).all()
    else:
        products = Product.query.filter_by(is_available=True).all()
    return render_template('home.html', products=products, search_query=search_query)
