from flask import Blueprint, session, jsonify, redirect, url_for, request, render_template
from model import Product, Review
from flask_login import login_required, current_user

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Only buyers can add to cart
    if current_user.role != 'Buyer':
        return jsonify({'error': 'Only buyers can add to cart.'}), 403
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})
    cart_item = cart.get(str(product_id), {'quantity': 0})
    cart_item['quantity'] += 1
    cart[str(product_id)] = cart_item
    session['cart'] = cart
    session.modified = True
    return jsonify({'success': True, 'message': f'Added {product.name} to cart.'})

@cart_bp.route('/', methods=['GET'])
@login_required
def view_cart():
    cart = session.get('cart', {})
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []
    cart_items = []
    for product in products:
        quantity = cart.get(str(product.id), {}).get('quantity', 1)
        reviews = Review.query.filter_by(product_id=product.id).all()
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'reviews': reviews
        })
    return render_template('cart.html', cart_items=cart_items)
