
from datetime import timedelta
from models import Booking

def check_conflict(hall_id, start_time, end_time):
    """
    Checks if a booking conflicts with existing APPROVED bookings.
    Includes a 15-minute buffer before and after the requested slot.
    """
    # Define buffer duration
    buffer = timedelta(minutes=15)

    # Adjust start and end times with buffer
    start_with_buffer = start_time - buffer
    end_with_buffer = end_time + buffer

    # Query for overlapping approved bookings
    # Overlap logic: (StartA <= EndB) and (EndA >= StartB)
    overlapping_booking = Booking.query.filter(
        Booking.hall_id == hall_id,
        Booking.status == 'APPROVED',
        Booking.start_ts < end_with_buffer,
        Booking.end_ts > start_with_buffer
    ).first()

    return overlapping_booking is not None
