from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required

payment_bp = Blueprint('payment', __name__)

from flask_login import current_user
from model import db, Order, OrderItem, Product, User

@payment_bp.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('cart.view_cart'))
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []
    total_price = 0
    order_items = []
    for product in products:
        quantity = cart.get(str(product.id), {}).get('quantity', 1)
        subtotal = product.price * quantity
        total_price += subtotal
        order_items.append({
            'product_id': product.id,
            'product_name': product.name,
            'farmer_id': product.farmer_id,
            'farmer_name': product.farmer.username if product.farmer else '',
            'quantity': quantity,
            'unit': product.unit,
            'price_at_purchase': product.price,
            'subtotal': subtotal
        })
    # Create Order
    order = Order(
        buyer_id=current_user.id,
        total_amount=total_price
    )
    db.session.add(order)
    db.session.flush()  # Get order.id
    # Create OrderItems
    for item in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            product_name=item['product_name'],
            farmer_id=item['farmer_id'],
            farmer_name=item['farmer_name'],
            quantity=item['quantity'],
            unit=item['unit'],
            price_at_purchase=item['price_at_purchase'],
            subtotal=item['subtotal']
        )
        db.session.add(order_item)
    db.session.commit()
    # Clear cart
    session['cart'] = {}
    session.modified = True
    return redirect(url_for('home.home'))

@payment_bp.route('/payment', methods=['GET'])
@login_required
def payment():
    # Use total from query param if present, else fallback to session cart calculation
    total = request.args.get('total', type=float)
    if total is None:
        cart = session.get('cart', {})
        product_ids = [int(pid) for pid in cart.keys()]
        from model import Product
        products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []
        total = 0
        for product in products:
            quantity = cart.get(str(product.id), {}).get('quantity', 1)
            total += product.price * quantity
    return render_template('payment.html', total_amount=total)
