from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from model import Product

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_authenticated and current_user.role == 'Farmer':
        return redirect('/dashboard')  # Only redirect farmers to dashboard
    
    # Sample products for the home page
    sample_products = [
        {
            'name': 'Fresh Organic Tomatoes',
            'description': 'Locally grown organic tomatoes, perfect for salads and cooking',
            'price': 2.99,
            'image': 'https://images.unsplash.com/photo-1546094097-5c2bfd3a5b89?w=500&auto=format&fit=crop&q=60',
            'farmer': 'John\'s Organic Farm'
        },
        {
            'name': 'Sweet Corn',
            'description': 'Fresh sweet corn, harvested at peak ripeness',
            'price': 1.99,
            'image': 'https://images.unsplash.com/photo-1601593768799-76c3c5aef2a2?w=500&auto=format&fit=crop&q=60',
            'farmer': 'Green Valley Farms'
        },
        {
            'name': 'Organic Carrots',
            'description': 'Crisp and sweet organic carrots, perfect for snacking',
            'price': 1.49,
            'image': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=500&auto=format&fit=crop&q=60',
            'farmer': 'Sunny Side Produce'
        },
        {
            'name': 'Fresh Lettuce',
            'description': 'Crisp and fresh lettuce, ideal for salads',
            'price': 1.99,
            'image': 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=500&auto=format&fit=crop&q=60',
            'farmer': 'Green Thumb Gardens'
        },
        {
            'name': 'Organic Potatoes',
            'description': 'Fresh organic potatoes, perfect for any recipe',
            'price': 2.49,
            'image': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=500&auto=format&fit=crop&q=60',
            'farmer': 'Harvest Time Farms'
        },
        {
            'name': 'Fresh Spinach',
            'description': 'Nutrient-rich spinach, perfect for salads and cooking',
            'price': 2.29,
            'image': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=500&auto=format&fit=crop&q=60',
            'farmer': 'Leafy Greens Farm'
        }
    ]
    
    return render_template('home.html', products=sample_products)