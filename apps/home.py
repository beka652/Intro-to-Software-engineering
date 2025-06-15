from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from model import Product, User

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_authenticated and current_user.role == 'Farmer':
        return redirect('/dashboard')  # Only redirect farmers to dashboard
    
    # Fetch all available products from the database
    products = Product.query.filter_by(is_available=True).all()
    
    # Format products for display
    product_list = []
    for product in products:
        farmer = User.query.get(product.farmer_id)
        # Construct the image URL properly
        if product.image_path:
            # The image_path is relative to static/uploads
            image_url = url_for('static', filename=f'uploads/{product.image_path}')
            print(f"Debug - Image path: {product.image_path}, URL: {image_url}")  # Debug line
        else:
            image_url = url_for('static', filename='images/no-image.png')
        
        product_list.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image_url': image_url,
            'farmer': farmer.username if farmer else 'Unknown Farmer',
            'quantity': product.quantity,
            'unit': 'units'  # Default unit since it's not in the model
        })
    
    return render_template('home.html', products=product_list)