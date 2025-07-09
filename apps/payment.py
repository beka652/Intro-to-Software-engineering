from flask import Blueprint, render_template
from flask_login import login_required

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment', methods=['GET'])
@login_required
def payment():
    return render_template('payment.html')
