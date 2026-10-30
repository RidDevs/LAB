"""
Student Attendance API - Application Entry Point.
Flask application initialization and blueprint registration.
"""

from flask import Flask, jsonify
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp


def create_app(test_config=None) -> Flask:
    """
    Application factory for the Flask app.
    
    :param test_config: Optional configuration dictionary for testing.
    :return: Configured Flask application instance.
    """
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    # Register blueprints
    app.register_blueprint(student_bp)
    app.register_blueprint(attendance_bp)

    # Welcome / Root route
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "message": "Student Attendance API is running.",
            "version": "1.0",
            "endpoints": {
                "POST /students": "Add a new student",
                "GET /students": "View all registered students",
                "GET /students/<student_id>": "View student details by ID",
                "POST /attendance": "Mark student attendance (Present/Absent)",
                "GET /attendance/<student_id>": "View attendance records for a student",
                "GET /attendance": "View all attendance records"
            }
        }), 200

    # Custom JSON error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": getattr(error, "description", "The request was invalid.")
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": getattr(error, "description", "The requested resource was not found.")
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": getattr(error, "description", "The HTTP method is not allowed for this URL.")
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server."
        }), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

