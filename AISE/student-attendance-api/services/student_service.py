"""
Student Service module.
Handles in-memory storage and business logic for students.
"""

from typing import Any, Dict, List, Optional


class StudentAlreadyExistsError(Exception):
    """Raised when attempting to add a student whose ID or roll number already exists."""
    pass


class StudentNotFoundError(Exception):
    """Raised when a requested student cannot be found."""
    pass


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


# In-memory store: student_id -> student dict
_students: Dict[str, dict] = {}


def add_student(student_id: Optional[Any] = None, name: Any = None, roll_number: Optional[Any] = None) -> dict:
    """
    Add a new student to the in-memory database.
    If student_id is omitted, roll_number is used as the student_id.
    
    :param student_id: Unique identifier for the student (string or integer, optional if roll_number provided).
    :param name: Student's full name (string).
    :param roll_number: Optional roll number (string or integer).
    :return: Created student dictionary.
    :raises ValidationError: If inputs are invalid or neither student_id nor roll_number is provided.
    :raises StudentAlreadyExistsError: If student_id or roll_number is already in use.
    """
    # If student_id is not provided, fall back to roll_number
    if student_id is None or (isinstance(student_id, str) and not student_id.strip()):
        student_id = roll_number

    # Validate student_id
    if student_id is None or isinstance(student_id, bool) or not isinstance(student_id, (str, int)):
        raise ValidationError("Field 'student_id' or 'roll_number' is required and must be a non-empty string or integer.")

    cleaned_id = str(student_id).strip()
    if not cleaned_id:
        raise ValidationError("Field 'student_id' or 'roll_number' cannot be empty or whitespace.")

    # Validate name
    if name is None or not isinstance(name, str) or not name.strip():
        raise ValidationError("Field 'name' is required and must be a non-empty string.")

    cleaned_name = name.strip()

    # Validate roll_number
    if roll_number is not None:
        if isinstance(roll_number, bool) or not isinstance(roll_number, (str, int)):
            raise ValidationError("Field 'roll_number' must be a string or integer if provided.")
        cleaned_roll = str(roll_number).strip()
        if not cleaned_roll:
            cleaned_roll = None
    else:
        cleaned_roll = None

    if cleaned_id in _students:
        raise StudentAlreadyExistsError(f"Student with ID '{cleaned_id}' already exists.")

    if cleaned_roll:
        for existing in _students.values():
            if existing.get("roll_number") == cleaned_roll:
                raise StudentAlreadyExistsError(f"Student with roll number '{cleaned_roll}' already exists.")

    student = {
        "student_id": cleaned_id,
        "name": cleaned_name,
        "roll_number": cleaned_roll
    }
    _students[cleaned_id] = student
    return student


def get_all_students() -> List[dict]:
    """
    Retrieve all registered students.
    
    :return: List of student dictionaries.
    """
    return list(_students.values())


def get_student_by_id(student_id: Any) -> dict:
    """
    Retrieve a single student by ID or roll number.
    
    :param student_id: The ID or roll number of the student.
    :return: Student dictionary.
    :raises ValidationError: If student_id is missing or invalid.
    :raises StudentNotFoundError: If student is not found.
    """
    if student_id is None or isinstance(student_id, bool) or not isinstance(student_id, (str, int)):
        raise ValidationError("Field 'student_id' is required and must be a string or integer.")

    cleaned_id = str(student_id).strip()
    if not cleaned_id:
        raise ValidationError("Field 'student_id' cannot be empty or whitespace.")

    # Primary lookup by student_id
    if cleaned_id in _students:
        return _students[cleaned_id]

    # Secondary lookup by roll_number
    for student in _students.values():
        if student.get("roll_number") == cleaned_id:
            return student

    raise StudentNotFoundError(f"Student with ID '{cleaned_id}' was not found.")


def student_exists(student_id: Any) -> bool:
    """
    Check if a student exists by student_id or roll_number.
    
    :param student_id: The ID or roll number of the student.
    :return: True if the student exists, False otherwise.
    """
    if student_id is None or isinstance(student_id, bool) or not isinstance(student_id, (str, int)):
        return False
    cleaned_id = str(student_id).strip()
    if cleaned_id in _students:
        return True
    for student in _students.values():
        if student.get("roll_number") == cleaned_id:
            return True
    return False


def clear_students() -> None:
    """Clear all stored students (useful for resetting state during tests)."""
    _students.clear()
