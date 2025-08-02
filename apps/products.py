from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from model import db, Product, Review, Reply, User
from werkzeug.utils import secure_filename
import os
from flask import jsonify

products_bp = Blueprint('products', __name__)
UPLOAD_FOLDER = 'static/uploads'

@products_bp.route('', methods=['GET'])
@products_bp.route('/', methods=['GET'])
@login_required
def view_products():
    if current_user.role == 'Customer':
        # Get filter parameters from the query string
        price_min = request.args.get('price_min', type=float)
        price_max = request.args.get('price_max', type=float)
        category = request.args.get('category')
        location = request.args.get('location')

        # Start with all available products
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
        products = query.all()
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
        unit = request.form.get('unit')
        
        # Handle product image
        image = request.files.get('image')
        image_path = None
        if image and image.filename:
            # Create user's product directory
            user_product_dir = os.path.join(UPLOAD_FOLDER, current_user.email)
            os.makedirs(user_product_dir, exist_ok=True)
            
            # Save the image
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_user.email, filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_path))
            print(f"Debug - Saved image to: {os.path.join(UPLOAD_FOLDER, image_path)}")  # Debug line
        
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            unit=unit,
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

        # Handle unit/measurement
        selected_unit = request.form.get('unit')
        custom_unit = request.form.get('unit_other')
        if selected_unit == 'Other' and custom_unit:
            product.unit = custom_unit.strip()
        elif selected_unit:
            product.unit = selected_unit
        else:
            product.unit = 'Unit'  # fallback default

        # Handle product image update
        image = request.files.get('image')
        if image and image.filename:
            # Create user's product directory
            user_product_dir = os.path.join(UPLOAD_FOLDER, current_user.email)
            os.makedirs(user_product_dir, exist_ok=True)

            # Delete old image if it exists
            if product.image_path:
                old_image_path = os.path.join(UPLOAD_FOLDER, product.image_path)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Save the new image
            filename = secure_filename(image.filename)
            product.image_path = os.path.join(current_user.email, filename)
            image.save(os.path.join(UPLOAD_FOLDER, product.image_path))
            print(f"Debug - Updated image to: {os.path.join(UPLOAD_FOLDER, product.image_path)}")  # Debug line

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

@products_bp.route('/review/<int:product_id>', methods=['POST'])
@login_required
def submit_review(product_id):
    if current_user.role != 'Buyer':
        return jsonify({'error': 'Only buyers can submit reviews.'}), 403
    data = request.get_json() or request.form
    rating = int(data.get('rating', 0))
    comment = data.get('feedback', '').strip()
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Invalid rating.'}), 400
    if not comment:
        return jsonify({'error': 'Feedback required.'}), 400
    # Prevent duplicate review by same user for same product
    existing = Review.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if existing:
        return jsonify({'error': 'You have already reviewed this product.'}), 400
    review = Review(product_id=product_id, user_id=current_user.id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Review submitted.'})

@products_bp.route('/reply/<int:review_id>', methods=['POST'])
@login_required
def submit_reply(review_id):
    if current_user.role != 'Farmer':
        return jsonify({'error': 'Only farmers can reply.'}), 403
    data = request.get_json() or request.form
    reply_text = data.get('reply', '').strip()
    if not reply_text:
        return jsonify({'error': 'Reply required.'}), 400
    review = Review.query.get_or_404(review_id)
    # Only the farmer who owns the product can reply
    if review.product.farmer_id != current_user.id:
        return jsonify({'error': 'Not authorized.'}), 403
    reply = Reply(review_id=review_id, farmer_id=current_user.id, reply_text=reply_text)
    db.session.add(reply)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Reply submitted.'})

# Helper to serialize reviews and replies for frontend

def serialize_review(review):
    return {
        'id': review.id,
        'buyer': {
            'id': review.reviewer.id,
            'username': review.reviewer.username,
            'email': review.reviewer.email
        },
        'rating': review.rating,
        'text': review.comment,
        'date_posted': review.date_posted.strftime('%Y-%m-%d %H:%M'),
        'replies': [
            {
                'id': reply.id,
                'farmer': {
                    'id': reply.farmer.id,
                    'username': reply.farmer.username,
                    'email': reply.farmer.email
                },
                'text': reply.reply_text,
                'date_posted': reply.date_posted.strftime('%Y-%m-%d %H:%M')
            } for reply in review.replies
        ]
    }

@products_bp.route('/reviews/<int:product_id>')
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    user_review = None
    has_rated = False
    if current_user.is_authenticated and current_user.role == 'Buyer':
        user_review = Review.query.filter_by(product_id=product_id, user_id=current_user.id).first()
        has_rated = user_review is not None
    return jsonify({
        'comments': [serialize_review(r) for r in reviews],
        'has_rated': has_rated,
        'user_review': serialize_review(user_review) if user_review else None
    })