from app import create_app, db

app = create_app()

# Ensure tables exist on startup (simple approach for this project scope)
with app.app_context():
    db.create_all()
