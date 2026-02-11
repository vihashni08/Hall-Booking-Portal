
from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_booking_email(recipient_email, subject, html_body, text_body=None):
    try:
        msg = Message(subject, recipients=[recipient_email])
        msg.body = text_body or "Please enable HTML to view this email."
        msg.html = html_body
        # In a real app, this would be asynchronous
        mail.send(msg)
        print(f"Email sent to {recipient_email}: {subject}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        print("--- DEBUG EMAIL CONTENT ---")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print(html_body)
        print("---------------------------")

def get_email_template(title, content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f6f9; margin: 0; padding: 0; }}
            .email-container {{ max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border: 1px solid #e1e4e8; }}
            .header {{ background-color: #00356b; color: #ffffff; padding: 20px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
            .content {{ padding: 30px; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #6c757d; border-top: 1px solid #eee; }}
            .details-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            .details-table td {{ padding: 10px; border-bottom: 1px solid #eee; }}
            .label {{ font-weight: 600; color: #555; width: 120px; }}
            .status-badge {{ display: inline-block; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 14px; }}
            .status-pending {{ background-color: #fff3cd; color: #856404; }}
            .status-approved {{ background-color: #d4edda; color: #155724; }}
            .status-rejected {{ background-color: #f8d7da; color: #721c24; }}
            .btn {{ display: inline-block; background-color: #00356b; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>🏫 SSN Hall Booking Portal</h1>
            </div>
            <div class="content">
                <h2>{title}</h2>
                {content}
            </div>
            <div class="footer">
                &copy; 2024 SSN Hall Booking Portal. This is an automated message.<br>
                Please do not reply to this email.
            </div>
        </div>
    </body>
    </html>
    """

def notify_admin_new_booking(booking):
    # In a real app, you might email all admins or a specific list
    # For now, we'll just print to console or try to send if configured
    print(f"New booking request from {booking.user.email} for {booking.hall.name}")

def notify_user_booking_submitted(booking):
    subject = f"Booking Received: {booking.event_name}"
    
    # Format dates
    start_str = booking.start_ts.strftime('%B %d, %Y at %I:%M %p')
    end_str = booking.end_ts.strftime('%B %d, %Y at %I:%M %p')
    
    content = f"""
    <p>Dear {booking.user.name},</p>
    <p>Your booking request has been successfully submitted and is currently <strong>PENDING</strong> review.</p>
    
    <table class="details-table">
        <tr><td class="label">Event:</td><td>{booking.event_name}</td></tr>
        <tr><td class="label">Type:</td><td>{booking.event_type}</td></tr>
        <tr><td class="label">Venue:</td><td>{booking.hall.name}</td></tr>
        <tr><td class="label">From:</td><td>{start_str}</td></tr>
        <tr><td class="label">To:</td><td>{end_str}</td></tr>
        <tr><td class="label">Status:</td><td><span class="status-badge status-pending">PENDING</span></td></tr>
    </table>
    
    <p>You will receive another email once an administrator reviews your request.</p>
    """
    
    html = get_email_template("Booking Confirmation", content)
    send_booking_email(booking.user.email, subject, html, "Booking received.")

def notify_user_status_change(booking):
    status_emoji = "✅" if booking.status == "APPROVED" else "❌"
    subject = f"Booking {booking.status}: {booking.event_name}"
    
    status_class = f"status-{booking.status.lower()}"
    
    start_str = booking.start_ts.strftime('%B %d, %Y at %I:%M %p')
    end_str = booking.end_ts.strftime('%B %d, %Y at %I:%M %p')
    
    content = f"""
    <p>Dear {booking.user.name},</p>
    <p>Your booking request status has been updated.</p>
    
    <div style="text-align: center; margin: 20px 0;">
        <span class="status-badge {status_class}" style="font-size: 18px; padding: 10px 20px;">
            {status_emoji} {booking.status}
        </span>
    </div>
    
    <table class="details-table">
        <tr><td class="label">Event:</td><td>{booking.event_name}</td></tr>
        <tr><td class="label">Venue:</td><td>{booking.hall.name}</td></tr>
        <tr><td class="label">From:</td><td>{start_str}</td></tr>
        <tr><td class="label">To:</td><td>{end_str}</td></tr>
    </table>
    
    <p>You can view your booking details in the portal.</p>
    """
    
    html = get_email_template(f"Booking {booking.status}", content)
    send_booking_email(booking.user.email, subject, html, f"Your booking is {booking.status}.")
