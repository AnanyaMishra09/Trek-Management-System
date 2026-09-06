from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity

from cache import cache_invalidate
from decorators import role_required
from extensions import db
from models.booking import Booking

history_bp = Blueprint("history", __name__, url_prefix="/api/history")


def booking_dict(b):
    return {
        "id": b.id,
        "status": b.status,
        "cancel_reason": b.cancel_reason,
        "booked_at": b.booked_at.isoformat(),
        "trek": {"id": b.trek.id, "name": b.trek.name, "location": b.trek.location, "status": b.trek.status},
        "user": {"id": b.user.id, "name": b.user.name, "email": b.user.email},
    }


@history_bp.get("/bookings")
@role_required("trekker", "admin")
def list_bookings():
    query = Booking.query
    if get_jwt().get("role") == "trekker":
        query = query.filter_by(user_id=get_jwt_identity())
    bookings = query.order_by(Booking.booked_at.desc()).all()
    return jsonify([booking_dict(b) for b in bookings])


@history_bp.post("/bookings/<int:booking_id>/cancel")
@role_required("trekker")
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403
    if booking.status != "Booked":
        return jsonify({"error": "booking is not active"}), 400

    booking.status = "Cancelled"
    booking.trek.slots += 1
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(booking_dict(booking))
