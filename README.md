# 🏫 SSN Hall Booking Portal

A robust, full-stack web application designed to streamline the process of booking seminar halls and auditoriums at SSN. This portal serves Faculty, Club Heads, and Administrators with a priority-based scheduling system.

## 🚀 Features

### for Users (Faculty & Club Heads)
- **Role-Based Priority:** Faculty bookings take precedence over Club events.
- **Smart Booking Form:** 
    - **Visual Availability Checker:** Interactive timeline shows real-time availability (Free/Pending/Booked) to prevent conflicts before submission.
    - **Event Details:** Captures comprehensive event information (Type, Name, Organizer).
- **Email Notifications:** Instant HTML-formatted confirmation emails upon request submission and status updates.
- **My Bookings:** dedicated dashboard to track personal booking history and status.

### for Administrators
- **Admin Dashboard:** Centralized view of all Pending and Approved bookings.
- **One-Click Actions:** Approve or Reject requests directly from the dashboard.
- **Conflict Management:** The system automatically flags conflicts, considering a 15-minute buffer between events.

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** HTML5, CSS3 (Yale Blue & Gold Theme), JavaScript (Vanilla)
- **Authentication:** Session-based (Flask-Session)
- **Email Service:** SMTP (Gmail) with HTML Templates

## 📂 Project Structure

```
backend/
 ├── app.py                 # Application entry point
 ├── config.py              # Configuration & Environment variables
 ├── models.py              # SQLAlchemy Database Models
 ├── reset_db.py            # Script to reset/seed database
 ├── requirements.txt       # Python dependencies
 ├── routes/                # Blueprint routes
 │   ├── auth.py            # Login/Logout
 │   ├── booking.py         # Booking logic & Availability API
 │   └── admin.py           # Admin controls
 ├── services/              # Business logic
 │   ├── conflict_checker.py # Algorithm for overlapping times
 │   └── email_service.py   # Email dispatch & Templates
 ├── templates/             # Jinja2 HTML Templates
 └── static/                # CSS & Client-side assets
```

## ⚡ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/vihashni08/Hall-Booking-Portal.git
cd Hall-Booking-Portal
```

### 2. Install Dependencies
It's recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Configure Database & Environment
1.  Ensure PostgreSQL is running and create a database named `seminar_hall_db`.
2.  Create a `.env` file in the `backend/` directory with the following content:
    ```
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgresql://postgres:password@localhost/seminar_hall_db
    MAIL_USERNAME=your-email@gmail.com
    MAIL_PASSWORD=your-app-password
    ```
3.  Update the values with your actual credentials.

### 4. Initialize Database
*Note: This step is now automated for Render deployment. The app will automatically create and seed the database on its first run.*

To do it manually on your local machine:
```bash
cd backend
python reset_db.py
```

### 5. Email Configuration (Optional)
To enable real email sending, update `backend/config.py` with your Gmail App Password.
*Note: If not configured, emails will be printed to the console for debugging.*

## 🏃‍♂️ Running the Application

```bash
cd backend
python app.py
```
The application will launch at `http://127.0.0.1:5000`.

## 🔑 Default Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `vihashni08@gmail.com` | `admin` |
| **Faculty** | `faculty@ssn.edu.in` | `faculty` |
| **Faculty** | `venkatanavadeep2310116@ssn.edu.in` | `hello` |
| **Club Head** | `vihashni2310922@ssn.edu.in` | `hello` |

## 🚀 Deployment (Render.com)

### Option 1: Blueprint (Automated)
*Note: Render might ask for a credit card for identity verification even for free plans.*
1.  **New Blueprint:** Select "New +" -> "Blueprint".
2.  Connect your repo.
3.  Render will auto-deploy using `render.yaml` (configured for Free tier).

### Option 2: Manual (Control)
1.  **Create Database:**
    - New + -> **PostgreSQL**.
    - Name: `ssn-hall-db`, Plan: **Free**.
    - Copy the `Internal Database URL`.
2.  **Create Web Service:**
    - New + -> **Web Service**.
    - Connect Repo.
    - Runtime: **Python**.
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `cd backend && gunicorn wsgi:app`
    - Plan: **Free**.
3.  **Environment Variables:**
    - Add `DATABASE_URL` (paste value from step 1).
    - Add `SECRET_KEY` (random string).
    - Add Email credentials.

## 📜 License
This project is developed for SSN internal use.
