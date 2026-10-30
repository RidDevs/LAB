"""
Unit and Integration Tests for Student Attendance API.
Tests cover all success paths, validation errors, edge cases, and status codes.
"""

import pytest
from app import create_app
from services.student_service import clear_students
from services.attendance_service import clear_attendance


@pytest.fixture
def app():
    """Create and configure a clean Flask app instance for testing."""
    test_app = create_app({"TESTING": True})
    return test_app


@pytest.fixture
def client(app):
    """Test client for issuing requests."""
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_in_memory_stores():
    """Reset in-memory data before and after each test function."""
    clear_students()
    clear_attendance()
    yield
    clear_students()
    clear_attendance()


# ============================================================================
# Root / Index Endpoint Tests
# ============================================================================

def test_root_endpoint(client):
    """Test that the index endpoint returns API status and endpoint directory."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert "message" in data
    assert "endpoints" in data


# ============================================================================
# Student Management Tests (Normal / Success Cases)
# ============================================================================

def test_add_student_success_with_all_fields(client):
    """Test adding a new student with string student_id, name, and roll_number."""
    payload = {
        "student_id": "S101",
        "name": "Alice Johnson",
        "roll_number": "CS-01"
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert data["message"] == "Student added successfully."
    assert data["student"]["student_id"] == "S101"
    assert data["student"]["name"] == "Alice Johnson"
    assert data["student"]["roll_number"] == "CS-01"


def test_add_student_with_numeric_id_and_roll_number(client):
    """Test adding a student with integer student_id and integer roll_number."""
    payload = {
        "student_id": 102,
        "name": "Bob Smith",
        "roll_number": 42
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["student"]["student_id"] == "102"
    assert data["student"]["roll_number"] == "42"


def test_add_student_with_alias_id_key(client):
    """Test adding a student using the 'id' key instead of 'student_id'."""
    payload = {
        "id": "S103",
        "name": "Charlie Brown"
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["student"]["student_id"] == "S103"


def test_add_student_with_only_name_and_roll_number(client):
    """Test adding student with only 'name' and 'roll_number' (roll_number becomes student_id)."""
    payload = {
        "name": "Rahul",
        "roll_number": "101"
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Student added successfully."
    assert data["student"]["name"] == "Rahul"
    assert data["student"]["roll_number"] == "101"
    assert data["student"]["student_id"] == "101"

    # Verify marking attendance using this roll_number / student_id
    att_res = client.post("/attendance", json={
        "student_id": "101",
        "status": "Present",
        "date": "2026-10-30"
    })
    assert att_res.status_code == 201
    assert att_res.get_json()["record"]["student_id"] == "101"


def test_add_student_without_optional_roll_number(client):
    """Test adding a student without supplying roll_number (defaults to None)."""
    payload = {
        "student_id": "S104",
        "name": "Diana Prince"
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["student"]["student_id"] == "S104"
    assert data["student"]["roll_number"] is None


def test_get_all_students_initially_empty(client):
    """Test retrieving all students when none have been added."""
    response = client.get("/students")
    assert response.status_code == 200
    data = response.get_json()
    assert data["students"] == []
    assert data["total"] == 0


def test_get_all_students_populated(client):
    """Test retrieving all students after adding multiple entries."""
    client.post("/students", json={"student_id": "S1", "name": "Alice"})
    client.post("/students", json={"student_id": "S2", "name": "Bob"})

    response = client.get("/students")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 2
    student_ids = [s["student_id"] for s in data["students"]]
    assert "S1" in student_ids
    assert "S2" in student_ids


def test_get_student_by_id_success(client):
    """Test retrieving an existing student by ID."""
    client.post("/students", json={"student_id": "S105", "name": "Eve Adams"})
    response = client.get("/students/S105")
    assert response.status_code == 200
    data = response.get_json()
    assert data["student"]["student_id"] == "S105"
    assert data["student"]["name"] == "Eve Adams"


# ============================================================================
# Student Management Tests (Validation & Error Cases)
# ============================================================================

def test_add_student_non_json_content_type(client):
    """Test rejecting non-JSON request body."""
    response = client.post("/students", data="not a json", content_type="text/plain")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"


def test_add_student_invalid_json_format_array(client):
    """Test rejecting JSON payload that is a list instead of an object."""
    response = client.post("/students", json=[{"student_id": "S1", "name": "Alice"}])
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"


def test_add_student_missing_student_id(client):
    """Test rejecting student creation when student_id is omitted."""
    response = client.post("/students", json={"name": "Alice"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"
    assert "student_id" in data["message"].lower()


def test_add_student_empty_whitespace_student_id(client):
    """Test rejecting student creation when student_id is whitespace."""
    response = client.post("/students", json={"student_id": "   ", "name": "Alice"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"


def test_add_student_boolean_student_id(client):
    """Test rejecting boolean value for student_id."""
    response = client.post("/students", json={"student_id": True, "name": "Alice"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"


def test_add_student_missing_name(client):
    """Test rejecting student creation when name is omitted."""
    response = client.post("/students", json={"student_id": "S106"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"
    assert "name" in data["message"].lower()


def test_add_student_non_string_name(client):
    """Test rejecting student creation when name is an integer."""
    response = client.post("/students", json={"student_id": "S107", "name": 12345})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"


def test_add_student_whitespace_name(client):
    """Test rejecting student creation when name is only whitespace."""
    response = client.post("/students", json={"student_id": "S108", "name": "     "})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"


def test_add_student_invalid_roll_number_type(client):
    """Test rejecting student creation when roll_number is a list/dictionary."""
    response = client.post("/students", json={"student_id": "S109", "name": "Frank", "roll_number": ["invalid"]})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"


def test_add_student_duplicate_id_conflict(client):
    """Test 409 Conflict when attempting to register an existing student ID."""
    client.post("/students", json={"student_id": "S200", "name": "Grace"})
    response = client.post("/students", json={"student_id": "S200", "name": "Grace Twin"})
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Conflict"
    assert "already exists" in data["message"].lower()


def test_get_nonexistent_student_not_found(client):
    """Test 404 Not Found when querying a non-existent student ID."""
    response = client.get("/students/UNKNOWN_ID")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not Found"


# ============================================================================
# Attendance Tests (Normal / Success Cases)
# ============================================================================

def test_mark_attendance_present_with_explicit_date(client):
    """Test marking a student as Present with a valid explicit date."""
    client.post("/students", json={"student_id": "S301", "name": "Hannah"})
    payload = {
        "student_id": "S301",
        "status": "Present",
        "date": "2026-10-30"
    }
    response = client.post("/attendance", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Attendance marked successfully."
    assert data["record"]["student_id"] == "S301"
    assert data["record"]["status"] == "Present"
    assert data["record"]["date"] == "2026-10-30"
    assert data["record"]["record_id"] == 1


def test_mark_attendance_absent_with_default_date(client):
    """Test marking a student as Absent without specifying date (defaults to today)."""
    client.post("/students", json={"student_id": "S302", "name": "Ian"})
    payload = {
        "student_id": "S302",
        "status": "Absent"
    }
    response = client.post("/attendance", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["record"]["status"] == "Absent"
    assert data["record"]["date"] is not None


def test_mark_attendance_case_insensitivity(client):
    """Test that lowercase and uppercase status values are normalized to Present/Absent."""
    client.post("/students", json={"student_id": "S303", "name": "Jack"})
    res1 = client.post("/attendance", json={"student_id": "S303", "status": "present", "date": "2026-10-25"})
    assert res1.status_code == 201
    assert res1.get_json()["record"]["status"] == "Present"

    res2 = client.post("/attendance", json={"student_id": "S303", "status": "ABSENT", "date": "2026-10-26"})
    assert res2.status_code == 201
    assert res2.get_json()["record"]["status"] == "Absent"


def test_mark_attendance_nested_route(client):
    """Test marking attendance via nested route /students/<student_id>/attendance."""
    client.post("/students", json={"student_id": "S304", "name": "Karen"})
    payload = {
        "status": "Present",
        "date": "2026-10-30"
    }
    response = client.post("/students/S304/attendance", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["record"]["student_id"] == "S304"
    assert data["record"]["status"] == "Present"


def test_view_student_attendance_records(client):
    """Test retrieving attendance history for an existing student via both routes."""
    client.post("/students", json={"student_id": "S305", "name": "Leo"})
    client.post("/attendance", json={"student_id": "S305", "status": "Present", "date": "2026-10-28"})
    client.post("/attendance", json={"student_id": "S305", "status": "Absent", "date": "2026-10-29"})

    # Via /attendance/<student_id>
    response = client.get("/attendance/S305")
    assert response.status_code == 200
    data = response.get_json()
    assert data["student_id"] == "S305"
    assert data["total_records"] == 2
    assert len(data["records"]) == 2

    # Via /students/<student_id>/attendance
    nested_response = client.get("/students/S305/attendance")
    assert nested_response.status_code == 200
    assert nested_response.get_json()["total_records"] == 2


def test_view_student_attendance_zero_records(client):
    """Test retrieving attendance for a student who has 0 attendance records."""
    client.post("/students", json={"student_id": "S306", "name": "Mia"})
    response = client.get("/attendance/S306")
    assert response.status_code == 200
    data = response.get_json()
    assert data["records"] == []
    assert data["total_records"] == 0


def test_list_all_attendance_records(client):
    """Test retrieving all attendance records across all students."""
    client.post("/students", json={"student_id": "S1", "name": "Alice"})
    client.post("/students", json={"student_id": "S2", "name": "Bob"})
    client.post("/attendance", json={"student_id": "S1", "status": "Present", "date": "2026-10-30"})
    client.post("/attendance", json={"student_id": "S2", "status": "Absent", "date": "2026-10-30"})

    response = client.get("/attendance")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_records"] == 2
    assert len(data["attendance"]) == 2


# ============================================================================
# Attendance Tests (Validation & Error Cases)
# ============================================================================

def test_mark_attendance_non_json_payload(client):
    """Test rejecting non-JSON payload when marking attendance."""
    response = client.post("/attendance", data="not json", content_type="text/plain")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"


def test_mark_attendance_invalid_json_array(client):
    """Test rejecting JSON array payload for attendance."""
    response = client.post("/attendance", json=[{"student_id": "S1", "status": "Present"}])
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"


def test_mark_attendance_unknown_student_not_found(client):
    """Test 404 Not Found when marking attendance for an unknown student ID."""
    payload = {
        "student_id": "NON_EXISTENT",
        "status": "Present",
        "date": "2026-10-30"
    }
    response = client.post("/attendance", json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not Found"
    assert "was not found" in data["message"]


def test_mark_attendance_nested_route_unknown_student(client):
    """Test 404 Not Found on nested route for unknown student ID."""
    response = client.post("/students/NON_EXISTENT/attendance", json={"status": "Present"})
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not Found"


def test_mark_attendance_missing_status(client):
    """Test rejecting attendance submission when status is omitted."""
    client.post("/students", json={"student_id": "S401", "name": "Noah"})
    payload = {"student_id": "S401"}
    response = client.post("/attendance", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"
    assert "status" in data["message"].lower()


def test_mark_attendance_invalid_status_value(client):
    """Test rejecting invalid attendance status values (e.g. 'Late', 'Excused')."""
    client.post("/students", json={"student_id": "S402", "name": "Olivia"})
    payload = {
        "student_id": "S402",
        "status": "Late",
        "date": "2026-10-30"
    }
    response = client.post("/attendance", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"
    assert "present" in data["message"].lower()


def test_mark_attendance_non_string_status(client):
    """Test rejecting non-string status (e.g. boolean or number)."""
    client.post("/students", json={"student_id": "S403", "name": "Paul"})
    response = client.post("/attendance", json={"student_id": "S403", "status": 1})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"


def test_mark_attendance_invalid_date_format_string(client):
    """Test rejecting date strings with incorrect format (e.g. DD-MM-YYYY)."""
    client.post("/students", json={"student_id": "S404", "name": "Quinn"})
    payload = {
        "student_id": "S404",
        "status": "Present",
        "date": "30-10-2026"
    }
    response = client.post("/attendance", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"
    assert "YYYY-MM-DD" in data["message"]


def test_mark_attendance_invalid_calendar_date(client):
    """Test rejecting dates with invalid calendar days (e.g. 2026-02-30)."""
    client.post("/students", json={"student_id": "S405", "name": "Rachel"})
    payload = {
        "student_id": "S405",
        "status": "Present",
        "date": "2026-02-30"
    }
    response = client.post("/attendance", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"
    assert "valid calendar date" in data["message"]


def test_mark_attendance_non_string_date(client):
    """Test rejecting non-string date types."""
    client.post("/students", json={"student_id": "S406", "name": "Sam"})
    payload = {
        "student_id": "S406",
        "status": "Present",
        "date": 20261030
    }
    response = client.post("/attendance", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Validation Error"


def test_mark_attendance_duplicate_same_date_conflict(client):
    """Test 409 Conflict when attempting to mark attendance twice for the same student on the same date."""
    client.post("/students", json={"student_id": "S407", "name": "Tina"})
    payload = {
        "student_id": "S407",
        "status": "Present",
        "date": "2026-10-30"
    }
    res1 = client.post("/attendance", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/attendance", json=payload)
    assert res2.status_code == 409
    data = res2.get_json()
    assert data["error"] == "Conflict"
    assert "already been recorded" in data["message"]


def test_view_attendance_unknown_student_not_found(client):
    """Test 404 Not Found when viewing attendance for an unknown student ID."""
    response = client.get("/attendance/UNKNOWN_STUDENT")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not Found"


def test_view_attendance_nested_unknown_student_not_found(client):
    """Test 404 Not Found on nested route for unknown student ID."""
    response = client.get("/students/UNKNOWN_STUDENT/attendance")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not Found"


# ============================================================================
# HTTP Error Handling Tests
# ============================================================================

def test_page_not_found_handler(client):
    """Test global 404 JSON response for undefined routes."""
    response = client.get("/non-existent-api-path")
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert data["error"] == "Not Found"


def test_method_not_allowed_handler(client):
    """Test global 405 JSON response when using an unsupported HTTP method."""
    response = client.delete("/students")
    assert response.status_code == 405
    assert response.is_json
    data = response.get_json()
    assert data["error"] == "Method Not Allowed"
