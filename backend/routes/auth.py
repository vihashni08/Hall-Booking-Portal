
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password: # Plain text comparison as requested
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name
            
            flash('Logged in successfully!', 'success')
            
            if user.role == 'ADMIN':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('booking.book_hall'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
