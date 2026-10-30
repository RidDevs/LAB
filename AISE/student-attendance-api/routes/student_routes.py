"""
Student Routes module.
Defines HTTP endpoints for managing students.
"""

from flask import Blueprint, jsonify, request
from services.student_service import (
    add_student,
    get_all_students,
    get_student_by_id,
    StudentAlreadyExistsError,
    StudentNotFoundError,
    ValidationError,
)

student_bp = Blueprint("student_bp", __name__)


@student_bp.route("/students", methods=["POST"])
def create_student():
    """
    Endpoint to add a new student.
    Expected JSON body:
    {
        "student_id": "S101",   (optional if roll_number is provided)
        "roll_number": "101",   (used as student_id if student_id is omitted)
        "name": "Alice Smith"
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

    student_id = data.get("student_id") if "student_id" in data else data.get("id")
    name = data.get("name")
    roll_number = data.get("roll_number")

    try:
        new_student = add_student(student_id=student_id, name=name, roll_number=roll_number)
        return jsonify({
            "message": "Student added successfully.",
            "student": new_student
        }), 201
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "message": str(err)}), 400
    except StudentAlreadyExistsError as err:
        return jsonify({"error": "Conflict", "message": str(err)}), 409


@student_bp.route("/students", methods=["GET"])
def list_students():
    """
    Endpoint to view all registered students.
    """
    students = get_all_students()
    return jsonify({
        "students": students,
        "total": len(students)
    }), 200


@student_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    """
    Endpoint to view details of a specific student by ID or roll number.
    """
    try:
        student = get_student_by_id(student_id)
        return jsonify({"student": student}), 200
    except StudentNotFoundError as err:
        return jsonify({"error": "Not Found", "message": str(err)}), 404
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "message": str(err)}), 400
