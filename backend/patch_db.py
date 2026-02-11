
from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Attempting to patch database schema...")
    try:
        # Try adding columns one by one. If they exist, it might fail, so we catch errors.
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE bookings ADD COLUMN IF NOT EXISTS event_name VARCHAR(200) DEFAULT 'Seminar' NOT NULL;"))
            conn.execute(text("ALTER TABLE bookings ADD COLUMN IF NOT EXISTS event_type VARCHAR(100) DEFAULT 'General' NOT NULL;"))
            conn.execute(text("ALTER TABLE bookings ADD COLUMN IF NOT EXISTS organizer_name VARCHAR(100) DEFAULT 'Unknown' NOT NULL;"))
            conn.commit()
            print("Schema patch applied successfully.")
    except Exception as e:
        print(f"Error patching schema: {e}")
