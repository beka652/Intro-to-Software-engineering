from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from model import Order

history_bp = Blueprint('history', __name__)

@history_bp.route('/')
@login_required
def history():
    if current_user.role != 'Buyer':
        return redirect(url_for('home.home'))
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('history.html', orders=orders)
