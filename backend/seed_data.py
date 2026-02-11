
from app import create_app
from models import db, User, SeminarHall

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()

    # check if users exist
    if User.query.first():
        print("Data already exists. Skipping seed.")
    else:
        print("Seeding users...")
        users = [
            User(name='Admin User', email='vihashni08@gmail.com', password='admin', role='ADMIN', priority=0),
            User(name='Faculty Member', email='faculty@ssn.edu.in', password='faculty', role='FACULTY', priority=1),
            User(name='Navadeep', email='venkatanavadeep2310116@ssn.edu.in', password='hello', role='FACULTY', priority=1),
            User(name='Club Head', email='vihashni2310922@ssn.edu.in', password='hello', role='CLUB', priority=2)
        ]
        
        db.session.add_all(users)
        
        print("Seeding halls...")
        halls = [
            SeminarHall(name='Main Auditorium', capacity=500),
            SeminarHall(name='Mini Hall 1', capacity=100),
            SeminarHall(name='Conference Room A', capacity=50)
        ]
        
        db.session.add_all(halls)
        
        db.session.commit()
        print("Database seeded successfully!")
