from flask import Blueprint, render_template
from flask_login import login_required, current_user
from model import Order, OrderItem, Product, Review

dashboard_bp = Blueprint('user_dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def dashboard():
    # Orders and stats for the current user (Buyer)
    orders = Order.query.filter_by(buyer_id=current_user.id).all()
    total_orders = len(orders)
    # Calculate total spent as the sum of all dashboard_total (same as in history)
    for order in orders:
        order.dashboard_total = sum(item.product.quantity * item.price_at_purchase for item in order.items)
    total_spent = sum(order.dashboard_total for order in orders)
    total_items = sum(sum(item.quantity for item in order.items) for order in orders)
    # Recent 5 orders, with formatted date for chart labels
    recent_orders = sorted(orders, key=lambda o: o.created_at, reverse=True)[:5]
    for order in recent_orders:
        order.formatted_month = order.created_at.strftime('%b %Y')
        order.formatted_datetime = order.created_at.strftime('%Y-%m-%d %H:%M')
        # Calculate total and quantity for each order for dashboard chart
        order.dashboard_quantity = sum(item.quantity for item in order.items)
        # Calculate total as in history.html (sum of item.product.quantity * item.price_at_purchase)
        order.dashboard_total = sum(item.product.quantity * item.price_at_purchase for item in order.items)
    # Product stats (if user is a Farmer)
    products = Product.query.filter_by(farmer_id=current_user.id).all() if current_user.role == 'Farmer' else []
    total_products = len(products)
    total_reviews = sum(len(p.reviews) for p in products) if products else 0
    avg_rating = round(sum(p.average_rating for p in products if p.reviews) / total_products, 2) if products and total_products else 0
    return render_template('user_dashboard.html',
        total_orders=total_orders,
        total_spent=total_spent,
        total_items=total_items,
        recent_orders=recent_orders,
        total_products=total_products,
        total_reviews=total_reviews,
        avg_rating=avg_rating,
        products=products
    )
