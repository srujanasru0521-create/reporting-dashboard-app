import os
import time
import uuid
import threading
import sys
import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

# Imports from Reporting Module
from modules.data_manager import load_reports, save_reports, filter_data
from modules.report_generator import generate_csv, generate_xlsx, generate_pdf
from modules.email_sender import send_email_with_attachment

# Imports from Notifications Module
from modules.database import create_tables
from modules.notifications_service import (
    create_notification, get_all_notifications, resolve_notification, 
    resolve_all_notifications_by_type, process_new_order_and_generate_alerts,
    test_email_configuration, create_deadline_notification_with_email
)
from modules.products_service import create_product, get_all_products

# This is the Flask server instance
app = Flask(__name__)
# Enable CORS to allow the frontend to make requests
CORS(app)

# Create the database tables on application startup
create_tables()

# --- Utility Functions (from Reporting Module) ---
def generate_and_send_report(report_data):
    """
    Handles the full report generation and email process.
    """
    print(f"Generating report for: {report_data['email']} in {report_data['format']} format...")
    report_data['status'] = 'Failed'
    try:
        filtered_data = filter_data(report_data)
        print(f"Found {len(filtered_data)} records for the report")
        file_extension = report_data['format'].lower()
        file_path = f"report_{report_data['id']}.{file_extension}"
        if file_extension == 'csv':
            generate_csv(filtered_data, file_path)
        elif file_extension == 'xlsx':
            generate_xlsx(filtered_data, file_path)
        elif file_extension == 'pdf':
            generate_pdf(filtered_data, file_path)
        print(f"Report file generated: {file_path}")
        success = send_email_with_attachment(report_data['email'], report_data['name'], file_path)
        reports = load_reports()
        for report in reports:
            if report['id'] == report_data['id']:
                report['status'] = 'Sent' if success else 'Failed'
                break
        save_reports(reports)
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"Report status for {report_data['name']} updated to {'Sent' if success else 'Failed'}")
    except Exception as e:
        print(f"**An unexpected error occurred during report generation or email sending:** {e}", file=sys.stderr)
        reports = load_reports()
        for report in reports:
            if report['id'] == report_data['id']:
                report['status'] = 'Failed'
                break
        save_reports(reports)

# --- Reporting Module Endpoints ---
@app.route('/reports', methods=['GET'])
def get_all_reports():
    """
    Handles GET requests to retrieve all reports from the "database".
    """
    try:
        reports = load_reports()
        return jsonify(reports)
    except Exception as e:
        print(f"Error in get_all_reports: {e}")
        return jsonify({"error": "Failed to load reports"}), 500

@app.route('/reports', methods=['POST'])
def create_report():
    """
    Handles POST requests to create a new report entry.
    """
    try:
        report_data = request.json
        if not report_data:
            return jsonify({"error": "No data provided"}), 400
        report_data['id'] = str(uuid.uuid4())
        report_data['createdAt'] = int(time.time() * 1000)
        report_data['status'] = 'Generating'
        reports = load_reports()
        reports.insert(0, report_data)
        save_reports(reports)
        print(f"New report request received: {report_data['name']}")
        thread = threading.Thread(target=generate_and_send_report, args=(report_data,))
        thread.start()
        return jsonify({"message": "Report generation started.", "id": report_data['id']}), 201
    except Exception as e:
        print(f"Error in create_report: {e}")
        return jsonify({"error": "Failed to create report"}), 500

# --- Notifications Module Endpoints ---
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """API endpoint to get all notifications."""
    notifications = get_all_notifications()
    return jsonify(notifications)

@app.route('/api/notifications', methods=['POST'])
def create_new_notification():
    """API endpoint to create a new notification."""
    data = request.json
    try:
        new_notification = create_notification(data)
        return jsonify(new_notification), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400

@app.route('/api/notifications/deadline', methods=['POST'])
def create_deadline_with_email():
    """API endpoint to create a deadline notification with email alert."""
    data = request.json
    try:
        new_notification = create_deadline_notification_with_email(data)
        return jsonify({
            "notification": new_notification,
            "message": "Deadline notification created and email sent successfully"
        }), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to create deadline notification: {str(e)}"}), 500

@app.route('/api/notifications/<notification_id>/resolve', methods=['PUT'])
def resolve_a_notification(notification_id):
    """API endpoint to resolve a notification."""
    rows_affected = resolve_notification(notification_id)
    if rows_affected > 0:
        return jsonify({"message": f"Notification {notification_id} resolved."})
    return jsonify({"message": f"Notification {notification_id} not found."}), 404

@app.route('/api/notifications/resolve_by_type/<alert_type>', methods=['PUT'])
def resolve_notifications_by_type(alert_type):
    """API endpoint to resolve all notifications of a given type."""
    rows_affected = resolve_all_notifications_by_type(alert_type)
    return jsonify({"message": f"Resolved {rows_affected} {alert_type} alerts."})

# --- API Endpoints for Products ---
@app.route('/api/products', methods=['GET'])
def get_products():
    """API endpoint to get all products."""
    products = get_all_products()
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def create_new_product():
    """API endpoint to create a new product."""
    data = request.json
    try:
        new_product = create_product(data)
        return jsonify(new_product), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400

# --- Combined Order Processing Endpoint ---
@app.route('/api/process_order', methods=['POST'])
def process_order():
    """
    API endpoint to process a new order and generate all relevant alerts.
    """
    data = request.json
    try:
        result = process_new_order_and_generate_alerts(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Email Testing Endpoint ---
@app.route('/api/test-email', methods=['POST'])
def test_email():
    """
    API endpoint to test email configuration.
    """
    try:
        success = test_email_configuration()
        if success:
            return jsonify({"message": "Test email sent successfully! Check your inbox."}), 200
        else:
            return jsonify({"error": "Failed to send test email. Check your email configuration."}), 500
    except Exception as e:
        return jsonify({"error": f"Email test failed: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Available endpoints:")
    print("- GET /reports - Get all reports")
    print("- POST /reports - Create new report")
    print("- GET /api/notifications - Get all notifications")
    print("- POST /api/notifications - Create a new notification")
    print("- PUT /api/notifications/<id>/resolve - Resolve a notification")
    print("- PUT /api/notifications/resolve_by_type/<type> - Resolve notifications by type")
    print("- POST /api/process_order - Process a new order and generate alerts")
    print("- GET /api/products - Get all products")
    print("- POST /api/products - Create a new product")
    print("- GET /health - Health check")
    app.run(debug=True, host='127.0.0.1', port=5000)













