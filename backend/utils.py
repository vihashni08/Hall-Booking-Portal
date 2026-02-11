
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'ADMIN':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def faculty_or_club_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] not in ['FACULTY', 'CLUB']:
             flash('Access denied. Faculty or Club Head only.', 'danger')
             return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
