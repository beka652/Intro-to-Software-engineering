from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def admin_page():
    if current_user.role != 'Admin':
        return "Access denied: Admins only!", 403
    return render_template('admin.html')