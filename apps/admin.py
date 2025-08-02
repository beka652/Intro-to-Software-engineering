from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from model import User, db

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Only Admins can access this route
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash("Access denied: Admins only.")
        return redirect(url_for('home.homepage'))  # redirect to home or error page
    
    users = User.query.all()
    return render_template('admin/admin_dashboard.html', users=users)

# Optional: Delete a user
@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'Admin':
        flash("Access denied.")
        return redirect(url_for('home.homepage'))
    
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted.")
    return redirect(url_for('admin.admin_dashboard'))
@admin_bp.route('/make-admin/<int:user_id>')
def make_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.role = 'Admin'
        db.session.commit()
        return f"{user.username} is now an Admin"
    return "User not found"
from werkzeug.security import generate_password_hash
