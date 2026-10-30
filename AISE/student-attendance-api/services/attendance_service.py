"""
Attendance Service module.
Handles in-memory storage and business logic for attendance records.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from services.student_service import get_student_by_id, StudentNotFoundError, ValidationError


class DuplicateAttendanceError(Exception):
    """Raised when attendance has already been recorded for a student on a specific date."""
    pass


# In-memory store: list of attendance record dictionaries
_attendance_records: List[dict] = []
_next_record_id: int = 1

VALID_STATUSES = {"present": "Present", "absent": "Absent"}


def mark_attendance(student_id: Any, status: Any, date: Optional[Any] = None) -> dict:
    """
    Record attendance for a student on a given date.
    
    :param student_id: ID or roll number of the student (string or integer).
    :param status: 'Present' or 'Absent' (case-insensitive string).
    :param date: Date in 'YYYY-MM-DD' format (optional, defaults to today's date).
    :return: Created attendance record dictionary.
    :raises ValidationError: If status or date format is invalid.
    :raises StudentNotFoundError: If student does not exist.
    :raises DuplicateAttendanceError: If attendance is already marked for that student on that date.
    """
    global _next_record_id

    # Validate student_id
    if student_id is None or isinstance(student_id, bool) or not isinstance(student_id, (str, int)):
        raise ValidationError("Field 'student_id' is required and must be a non-empty string or integer.")

    cleaned_student_id = str(student_id).strip()
    if not cleaned_student_id:
        raise ValidationError("Field 'student_id' cannot be empty or whitespace.")

    # Check student existence and resolve canonical student_id
    student = get_student_by_id(cleaned_student_id)
    canonical_student_id = student["student_id"]

    # Validate status
    if status is None or not isinstance(status, str) or not status.strip():
        raise ValidationError("Field 'status' is required and must be either 'Present' or 'Absent'.")

    normalized_status = VALID_STATUSES.get(status.strip().lower())
    if not normalized_status:
        raise ValidationError("Invalid status. Allowed values are 'Present' or 'Absent'.")

    # Validate date
    if date is None or (isinstance(date, str) and not date.strip()):
        record_date = datetime.now().strftime("%Y-%m-%d")
    elif isinstance(date, str):
        date_str = date.strip()
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            record_date = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            raise ValidationError("Field 'date' must be a valid calendar date in 'YYYY-MM-DD' format.")
    else:
        raise ValidationError("Field 'date' must be a string in 'YYYY-MM-DD' format.")

    # Check for duplicate record for the same student on the same date
    for record in _attendance_records:
        if record["student_id"] == canonical_student_id and record["date"] == record_date:
            raise DuplicateAttendanceError(
                f"Attendance for student '{canonical_student_id}' on {record_date} has already been recorded."
            )

    new_record = {
        "record_id": _next_record_id,
        "student_id": canonical_student_id,
        "date": record_date,
        "status": normalized_status
    }
    _next_record_id += 1
    _attendance_records.append(new_record)
    return new_record


def get_student_attendance(student_id: Any) -> List[dict]:
    """
    Retrieve all attendance records for a specific student.
    
    :param student_id: ID or roll number of the student.
    :return: List of attendance records for the student.
    :raises ValidationError: If student_id is invalid.
    :raises StudentNotFoundError: If student does not exist.
    """
    if student_id is None or isinstance(student_id, bool) or not isinstance(student_id, (str, int)):
        raise ValidationError("Field 'student_id' is required and must be a string or integer.")

    cleaned_student_id = str(student_id).strip()
    if not cleaned_student_id:
        raise ValidationError("Field 'student_id' cannot be empty or whitespace.")

    # Resolve student existence
    student = get_student_by_id(cleaned_student_id)
    canonical_student_id = student["student_id"]

    return [record for record in _attendance_records if record["student_id"] == canonical_student_id]


def get_all_attendance() -> List[dict]:
    """
    Retrieve all attendance records across all students.
    
    :return: List of all attendance records.
    """
    return list(_attendance_records)


def clear_attendance() -> None:
    """Clear all attendance records from memory (primarily for testing)."""
    global _next_record_id
    _attendance_records.clear()
    _next_record_id = 1
