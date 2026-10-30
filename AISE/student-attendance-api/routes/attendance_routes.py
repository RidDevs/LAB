"""
Attendance Routes module.
Defines HTTP endpoints for marking and viewing student attendance records.
"""

from flask import Blueprint, jsonify, request
from services.attendance_service import (
    mark_attendance,
    get_student_attendance,
    get_all_attendance,
    DuplicateAttendanceError,
)
from services.student_service import StudentNotFoundError, ValidationError

attendance_bp = Blueprint("attendance_bp", __name__)


@attendance_bp.route("/attendance", methods=["POST"])
def record_attendance():
    """
    Endpoint to mark a student as Present or Absent.
    Expected JSON body:
    {
        "student_id": "S101",
        "status": "Present" or "Absent",
        "date": "YYYY-MM-DD" (optional, defaults to current date)
    }
    """
    if not request.is_json:
        return jsonify({
            "error": "Bad Request",
            "message": "Request payload must be JSON with Content-Type 'application/json'."
        }), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "error": "Bad Request",
            "message": "Invalid JSON body format. A JSON object is required."
        }), 400

    student_id = data.get("student_id")
    status = data.get("status")
    date = data.get("date")

    try:
        record = mark_attendance(student_id=student_id, status=status, date=date)
        return jsonify({
            "message": "Attendance marked successfully.",
            "record": record
        }), 201
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "message": str(err)}), 400
    except StudentNotFoundError as err:
        return jsonify({"error": "Not Found", "message": str(err)}), 404
    except DuplicateAttendanceError as err:
        return jsonify({"error": "Conflict", "message": str(err)}), 409


@attendance_bp.route("/attendance/<student_id>", methods=["GET"])
def view_student_attendance(student_id):
    """
    Endpoint to view attendance records for a specific student by student_id.
    """
    try:
        records = get_student_attendance(student_id)
        return jsonify({
            "student_id": student_id,
            "records": records,
            "total_records": len(records)
        }), 200
    except StudentNotFoundError as err:
        return jsonify({"error": "Not Found", "message": str(err)}), 404
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "message": str(err)}), 400


@attendance_bp.route("/attendance", methods=["GET"])
def list_all_attendance():
    """
    Endpoint to view all attendance records across all students.
    """
    records = get_all_attendance()
    return jsonify({
        "attendance": records,
        "total_records": len(records)
    }), 200


@attendance_bp.route("/students/<student_id>/attendance", methods=["POST"])
def record_student_attendance_direct(student_id):
    """
    Nested RESTful endpoint to mark attendance directly for a student resource:
    POST /students/<student_id>/attendance
    Expected JSON body:
    {
        "status": "Present" or "Absent",
        "date": "YYYY-MM-DD" (optional)
    }
    """
    if not request.is_json:
        return jsonify({
            "error": "Bad Request",
            "message": "Request payload must be JSON with Content-Type 'application/json'."
        }), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "error": "Bad Request",
            "message": "Invalid JSON body format. A JSON object is required."
        }), 400

    status = data.get("status")
    date = data.get("date")

    try:
        record = mark_attendance(student_id=student_id, status=status, date=date)
        return jsonify({
            "message": "Attendance marked successfully.",
            "record": record
        }), 201
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "message": str(err)}), 400
    except StudentNotFoundError as err:
        return jsonify({"error": "Not Found", "message": str(err)}), 404
    except DuplicateAttendanceError as err:
        return jsonify({"error": "Conflict", "message": str(err)}), 409


@attendance_bp.route("/students/<student_id>/attendance", methods=["GET"])
def view_student_attendance_direct(student_id):
    """
    Nested RESTful endpoint to view attendance records for a specific student:
    GET /students/<student_id>/attendance
    """
    try:
        records = get_student_attendance(student_id)
        return jsonify({
            "student_id": student_id,
            "records": records,
            "total_records": len(records)
        }), 200
    except StudentNotFoundError as err:
        return jsonify({"error": "Not Found", "message": str(err)}), 404
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "message": str(err)}), 400
