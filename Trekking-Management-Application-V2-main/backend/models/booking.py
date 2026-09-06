from datetime import datetime

from extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"
    __table_args__ = (
        db.UniqueConstraint("user_id", "trek_id", name="uq_user_trek_booking"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Booked")  # Booked/Cancelled/Completed
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
    cancel_reason = db.Column(db.String(255), nullable=True)

    user = db.relationship("User")
    trek = db.relationship("Trek")
