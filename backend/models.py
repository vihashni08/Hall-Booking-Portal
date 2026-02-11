
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Plain text as requested (NOT recommended for prod)
    role = db.Column(db.String(20), nullable=False)  # ADMIN, FACULTY, CLUB
    priority = db.Column(db.Integer, nullable=False) # ADMIN=0, FACULTY=1, CLUB=2

    def __repr__(self):
        return f'<User {self.email}>'

class SeminarHall(db.Model):
    __tablename__ = 'seminar_halls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<SeminarHall {self.name}>'

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('seminar_halls.id'), nullable=False)
    start_ts = db.Column(db.DateTime, nullable=False)
    end_ts = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='PENDING')  # PENDING, APPROVED, REJECTED
    priority = db.Column(db.Integer, nullable=False) # Inherited from user at time of booking
    
    # New fields
    event_name = db.Column(db.String(200), nullable=False, default="Seminar")
    event_type = db.Column(db.String(100), nullable=False, default="General")
    organizer_name = db.Column(db.String(100), nullable=False, default="Unknown")

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    hall = db.relationship('SeminarHall', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Booking {self.id} - {self.status}>'
