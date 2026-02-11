
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from models import db, Booking, SeminarHall, User
from utils import login_required, faculty_or_club_required
from services.conflict_checker import check_conflict
from services.email_service import notify_admin_new_booking, notify_user_booking_submitted

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book', methods=['GET', 'POST'])
@login_required
@faculty_or_club_required
def book_hall():
    if request.method == 'POST':
        hall_id = request.form.get('hall_id')
        start_ts = request.form.get('start_ts')
        end_ts = request.form.get('end_ts')
        event_name = request.form.get('event_name')
        event_type = request.form.get('event_type')
        organizer_name = request.form.get('organizer_name')

        try:
            start_dt = datetime.strptime(start_ts, '%Y-%m-%dT%H:%M')
            end_dt = datetime.strptime(end_ts, '%Y-%m-%dT%H:%M')
            
            if start_dt >= end_dt:
                flash('End time must be after start time.', 'danger')
                return redirect(url_for('booking.book_hall'))

            if check_conflict(hall_id, start_dt, end_dt):
                flash('Hall is already booked for this time slot (including buffer).', 'danger')
                return redirect(url_for('booking.book_hall'))

            # Get user priority
            user = User.query.get(session['user_id'])
            
            new_booking = Booking(
                user_id=user.id,
                hall_id=hall_id,
                start_ts=start_dt,
                end_ts=end_dt,
                status='PENDING',
                priority=user.priority,
                event_name=event_name,
                event_type=event_type,
                organizer_name=organizer_name
            )
            
            db.session.add(new_booking)
            db.session.commit()
            
            notify_admin_new_booking(new_booking)
            notify_user_booking_submitted(new_booking)
            
            flash('Booking request submitted successfully!', 'success')
            return redirect(url_for('booking.my_bookings'))

        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('booking.book_hall'))

    halls = SeminarHall.query.all()
    return render_template('book_hall.html', halls=halls)

@booking_bp.route('/my_bookings')
@login_required
def my_bookings():
    user_id = session['user_id']
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.start_ts.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

@booking_bp.route('/schedule')
def schedule():
    bookings = Booking.query.filter_by(status='APPROVED').order_by(Booking.start_ts).all()
    return render_template('schedule.html', bookings=bookings)

@booking_bp.route('/check_availability')
@login_required
def check_availability():
    hall_id = request.args.get('hall_id')
    date_str = request.args.get('date')
    
    if not hall_id or not date_str:
         return jsonify({'error': 'Missing parameters'}), 400
         
    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_start = datetime.combine(query_date, datetime.min.time())
        day_end = datetime.combine(query_date, datetime.max.time())
        
        bookings = Booking.query.filter(
            Booking.hall_id == hall_id,
            Booking.status.in_(['APPROVED', 'PENDING']),
            Booking.end_ts > day_start,
            Booking.start_ts < day_end
        ).all()
        
        events = []
        for b in bookings:
            events.append({
                'start': b.start_ts.isoformat(),
                'end': b.end_ts.isoformat(),
                'status': b.status,
                'title': b.event_name
            })
            
        return jsonify(events)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
