from extensions import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy/Moderate/Hard
    duration_days = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    slots = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="Open")  # Open/Started/Completed/Closed
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    staff = db.relationship("User")
