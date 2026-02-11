
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Booking
from utils import admin_required
from services.email_service import notify_user_status_change

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    pending_bookings = Booking.query.filter_by(status='PENDING').order_by(Booking.priority, Booking.start_ts).all()
    all_bookings = Booking.query.order_by(Booking.start_ts.desc()).all()
    return render_template('admin_dashboard.html', pending_bookings=pending_bookings, all_bookings=all_bookings)

@admin_bp.route('/approve/<int:booking_id>')
@admin_required
def approve_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'APPROVED'
    db.session.commit()
    
    notify_user_status_change(booking)
    
    flash(f'Booking #{booking.id} approved.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject/<int:booking_id>')
@admin_required
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'REJECTED'
    db.session.commit()
    
    notify_user_status_change(booking)
    
    flash(f'Booking #{booking.id} rejected.', 'warning')
    return redirect(url_for('admin.dashboard'))
