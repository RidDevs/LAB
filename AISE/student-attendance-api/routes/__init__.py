"""Routes package for Student Attendance API."""
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp

__all__ = ["student_bp", "attendance_bp"]

