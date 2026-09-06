import os

from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import get_jwt_identity

from celery_app import celery
from decorators import role_required
from tasks import export_booking_history_csv

export_bp = Blueprint("export", __name__, url_prefix="/api/export")


@export_bp.post("/booking-history")
@role_required("trekker")
def trigger_export():
    task = export_booking_history_csv.apply_async(args=[get_jwt_identity()])
    return jsonify({"task_id": task.id}), 202


@export_bp.get("/booking-history/<task_id>")
@role_required("trekker")
def export_status(task_id):
    result = celery.AsyncResult(task_id)
    if not result.ready():
        return jsonify({"status": result.status})
    return jsonify({"status": "SUCCESS", "download_url": f"/api/export/booking-history/{task_id}/download"})


@export_bp.get("/booking-history/<task_id>/download")
@role_required("trekker")
def download_export(task_id):
    result = celery.AsyncResult(task_id)
    if not result.ready():
        return jsonify({"error": "not ready"}), 400
    path = result.get()
    if not os.path.exists(path):
        return jsonify({"error": "file not found"}), 404
    return send_file(path, as_attachment=True, download_name="booking_history.csv")
