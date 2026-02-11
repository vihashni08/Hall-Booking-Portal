
from app import create_app
from models import db, User, SeminarHall
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Starting HARD Database Reset...")
    
    # Force drop tables using raw SQL just in case SQLAlchemy metadata is out of sync
    try:
        with db.engine.connect() as conn:
            print("Dropping tables via raw SQL...")
            conn.execute(text("DROP TABLE IF EXISTS bookings CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS seminar_halls CASCADE;"))
            conn.commit()
            print("Tables dropped.")
    except Exception as e:
        print(f"Error dropping tables: {e}")

    print("Recreating all tables from models...")
    db.create_all()

    print("Seeding initial data...")
    # Seed Users
    if not User.query.first():
        users = [
            User(name='Admin User', email='vihashni08@gmail.com', password='admin', role='ADMIN', priority=0),
            User(name='Faculty Member', email='faculty@ssn.edu.in', password='faculty', role='FACULTY', priority=1),
            User(name='Club Head', email='vihashni2310922@ssn.edu.in', password='hello', role='CLUB', priority=2)
        ]
        db.session.add_all(users)
        
        # Seed Halls
        halls = [
            SeminarHall(name='Main Auditorium', capacity=500),
            SeminarHall(name='Mini Hall 1', capacity=100),
            SeminarHall(name='Conference Room A', capacity=50)
        ]
        db.session.add_all(halls)
        
        db.session.commit()
        print("Data seeded successfully!")
    else:
        print("Data already exists (unexpected after drop).")

    print("HARD RESET COMPLETE.")
