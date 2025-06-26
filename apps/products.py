from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from model import db, Product
from werkzeug.utils import secure_filename
import os
import logging

logging.basicConfig(level=logging.DEBUG)

products_bp = Blueprint('products', __name__)
UPLOAD_FOLDER = 'static/uploads'

@products_bp.route('/')
@login_required
def view_products():
    if current_user.role == 'Customer':
        # Show all available products for customers
        products = Product.query.filter_by(is_available=True).all()
        return render_template('products/view_products.html', products=products)
    elif current_user.role == 'Farmer':
        # Redirect farmers to their dashboard
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('home.home'))

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'Farmer':
        return redirect(url_for('home.home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        
        # Handle product image
        image = request.files.get('image')
        image_path = None
        if image and image.filename:
            import time
            filename = f"{current_user.id}_{int(time.time())}_{secure_filename(image.filename)}"
            image_path = filename
            image.save(os.path.join(UPLOAD_FOLDER, image_path))
            logging.debug(f"Saved image to: {os.path.join(UPLOAD_FOLDER, image_path)}")
        
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            image_path=image_path,
            farmer_id=current_user.id,
            is_available=True
        )
        
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('products/add_product.html')

@products_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.role != 'Farmer':
        return redirect(url_for('home.home'))
    
    product = Product.query.get_or_404(product_id)
    if product.farmer_id != current_user.id:
        return redirect(url_for('products.view_products'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.quantity = int(request.form.get('quantity'))
        product.is_available = bool(request.form.get('is_available'))
        
        # Handle product image update
        image = request.files.get('image')
        if image and image.filename:
            import time
            # Delete old image if it exists
            if product.image_path:
                old_image_path = os.path.join(UPLOAD_FOLDER, product.image_path)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            filename = f"{current_user.id}_{int(time.time())}_{secure_filename(image.filename)}"
            product.image_path = filename
            image.save(os.path.join(UPLOAD_FOLDER, product.image_path))
            logging.debug(f"Updated image to: {os.path.join(UPLOAD_FOLDER, product.image_path)}")
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('products/edit_product.html', product=product)

@products_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if current_user.role != 'Farmer':
        return redirect(url_for('home.home'))
    
    product = Product.query.get_or_404(product_id)
    if product.farmer_id != current_user.id:
        return redirect(url_for('products.view_products'))
    
    # Delete the product image if it exists
    if product.image_path:
        image_path = os.path.join(UPLOAD_FOLDER, product.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('dashboard.dashboard')) 