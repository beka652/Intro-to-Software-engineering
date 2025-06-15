from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from model import Product

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def dashboard():
    if current_user.role != 'Farmer':
        return redirect(url_for('home.home'))
    
    # Get farmer's products
    products = Product.query.filter_by(farmer_id=current_user.id).all()
    return render_template('dashboard.html', products=products)