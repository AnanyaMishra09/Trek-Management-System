from flask import Blueprint, jsonify, request

from cache import cache_invalidate
from decorators import role_required
from extensions import db
from models.trek import Trek
from models.user import User
from validators import is_valid_email, validate_trek_numbers

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def trek_dict(t):
    return {
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration_days": t.duration_days,
        "price": t.price,
        "slots": t.slots,
        "status": t.status,
        "staff_id": t.staff_id,
        "staff_name": t.staff.name if t.staff else None,
    }


def user_dict(u):
    return {"id": u.id, "name": u.name, "email": u.email, "role": u.role, "is_active": u.is_active}


@admin_bp.get("/treks")
@role_required("admin")
def list_treks():
    q = request.args.get("q")
    query = Trek.query
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Trek.name.ilike(like), Trek.location.ilike(like)))
    return jsonify([trek_dict(t) for t in query.all()])


@admin_bp.post("/treks")
@role_required("admin")
def create_trek():
    data = request.get_json() or {}
    required = ["name", "location", "difficulty", "duration_days", "price", "slots"]
    if any(data.get(f) in (None, "") for f in required):
        return jsonify({"error": f"required fields: {', '.join(required)}"}), 400
    if errors := validate_trek_numbers(data):
        return jsonify({"error": "; ".join(errors)}), 400

    trek = Trek(
        name=data["name"],
        location=data["location"],
        difficulty=data["difficulty"],
        duration_days=data["duration_days"],
        price=data["price"],
        slots=data["slots"],
    )
    db.session.add(trek)
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(trek_dict(trek)), 201


@admin_bp.put("/treks/<int:trek_id>")
@role_required("admin")
def update_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    data = request.get_json() or {}
    if errors := validate_trek_numbers(data):
        return jsonify({"error": "; ".join(errors)}), 400
    for field in ["name", "location", "difficulty", "duration_days", "price", "slots", "status"]:
        if field in data:
            setattr(trek, field, data[field])
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(trek_dict(trek))


@admin_bp.delete("/treks/<int:trek_id>")
@role_required("admin")
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify({"message": "deleted"})


@admin_bp.patch("/treks/<int:trek_id>/assign")
@role_required("admin")
def assign_staff(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    staff_id = (request.get_json() or {}).get("staff_id")
    staff = User.query.filter_by(id=staff_id, role="staff").first()
    if not staff:
        return jsonify({"error": "staff not found"}), 404
    trek.staff_id = staff.id
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(trek_dict(trek))


@admin_bp.get("/staff")
@role_required("admin")
def list_staff():
    query = User.query.filter_by(role="staff")
    if q := request.args.get("q"):
        like = f"%{q}%"
        query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
    return jsonify([user_dict(u) for u in query.all()])


@admin_bp.post("/staff")
@role_required("admin")
def create_staff():
    data = request.get_json() or {}
    name, email, password = data.get("name"), data.get("email"), data.get("password")
    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400
    if not is_valid_email(email):
        return jsonify({"error": "invalid email format"}), 400
    if len(password) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    staff = User(name=name, email=email, role="staff")
    staff.set_password(password)
    db.session.add(staff)
    db.session.commit()
    return jsonify(user_dict(staff)), 201


@admin_bp.get("/users")
@role_required("admin")
def list_users():
    query = User.query.filter_by(role="trekker")
    if q := request.args.get("q"):
        like = f"%{q}%"
        query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
    return jsonify([user_dict(u) for u in query.all()])


@admin_bp.patch("/users/<int:user_id>/toggle-active")
@role_required("admin")
def toggle_active(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify(user_dict(user))


@admin_bp.get("/stats")
@role_required("admin")
def stats():
    from models.booking import Booking

    return jsonify(
        {
            "treks": Trek.query.count(),
            "staff": User.query.filter_by(role="staff").count(),
            "trekkers": User.query.filter_by(role="trekker").count(),
            "bookings": Booking.query.count(),
        }
    )
