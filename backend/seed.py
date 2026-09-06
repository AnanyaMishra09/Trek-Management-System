"""One-time script: creates tables + the single hardcoded Admin user."""
from app import app
from extensions import db
from models.user import User

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="admin@trekking.com").first():
        admin = User(name="Admin", email="admin@trekking.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@trekking.com / admin123")
    else:
        print("Admin user already exists.")
