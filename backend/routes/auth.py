from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from extensions import db
from models.user import User
from validators import is_valid_email

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
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

    user = User(name=name, email=email, role="trekker")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "registered"}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email, password = data.get("email"), data.get("password")
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401
    if not user.is_active:
        return jsonify({"error": "account is blacklisted"}), 403

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({"token": token, "role": user.role, "name": user.name})
