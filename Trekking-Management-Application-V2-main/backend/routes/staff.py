from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from cache import cache_invalidate
from decorators import role_required
from extensions import db
from models.booking import Booking
from models.trek import Trek
from validators import validate_trek_numbers

staff_bp = Blueprint("staff", __name__, url_prefix="/api/staff")


def trek_dict(t, participant_count=None):
    d = {
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration_days": t.duration_days,
        "price": t.price,
        "slots": t.slots,
        "status": t.status,
    }
    if participant_count is not None:
        d["participant_count"] = participant_count
    return d


@staff_bp.get("/treks")
@role_required("staff")
def list_my_treks():
    staff_id = get_jwt_identity()
    treks = Trek.query.filter_by(staff_id=staff_id).all()
    return jsonify(
        [trek_dict(t, Booking.query.filter_by(trek_id=t.id, status="Booked").count()) for t in treks]
    )


@staff_bp.put("/treks/<int:trek_id>")
@role_required("staff")
def update_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    if errors := validate_trek_numbers(data):
        return jsonify({"error": "; ".join(errors)}), 400
    for field in ["slots", "status"]:
        if field in data:
            setattr(trek, field, data[field])
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(trek_dict(trek))


@staff_bp.patch("/treks/<int:trek_id>/status")
@role_required("staff")
def set_status(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    status = (request.get_json() or {}).get("status")
    valid_transitions = {"Open": ("Started", "Closed"), "Started": ("Completed", "Closed")}
    if status not in valid_transitions.get(trek.status, ()):
        return jsonify({"error": f"cannot move from {trek.status} to {status}"}), 400

    trek.status = status
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(trek_dict(trek))


@staff_bp.get("/treks/<int:trek_id>/participants")
@role_required("staff")
def participants(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    bookings = Booking.query.filter_by(trek_id=trek_id, status="Booked").all()
    return jsonify(
        [{"booking_id": b.id, "id": b.user.id, "name": b.user.name, "email": b.user.email} for b in bookings]
    )


@staff_bp.patch("/treks/<int:trek_id>/participants/<int:booking_id>/revoke")
@role_required("staff")
def revoke_participant(trek_id, booking_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    booking = Booking.query.filter_by(id=booking_id, trek_id=trek_id, status="Booked").first_or_404()
    reason = (request.get_json() or {}).get("reason", "").strip()
    if not reason:
        return jsonify({"error": "reason is required"}), 400

    booking.status = "Cancelled"
    booking.cancel_reason = reason
    trek.slots += 1
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify({"message": "booking revoked"})
