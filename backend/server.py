from flask import Flask, request, jsonify
from datetime import datetime
import json

# Assuming DatabaseManager is defined in a separate file, e.g., `database.py`
from sqlite import DatabaseManager  # Adjust the import path if necessary

app = Flask(__name__)

import os

from flask_cors import CORS

CORS(app)

def load_data(file_name):
    if not os.path.exists(file_name):
        print(f"File not found: {file_name}")
        return []
    try:
        with open(file_name, "r") as f:
            return f.readlines()
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return []


@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    """Authenticate a user based on email and password."""
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
    except (json.JSONDecodeError, TypeError):
        return jsonify({"error": "Invalid JSON data"}), 400

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db_manager = DatabaseManager(
        db_name='defaultdb',
        user='avnadmin',
        password='AVNS_U-c1ezivY9TcPqqXrwg',
        host='mysql-3ed7264d-execcsgo-bef4.f.aivencloud.com',
        port=18173
    )
    user = db_manager.get_user_by_email(email)

    print('found this')
    print(user)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Assuming the user tuple structure: (id, name, email, password)
    if user[3] != password:
        return jsonify({"error": "Invalid password"}), 400

    return jsonify({"success": "Authentication successful"}), 200

@app.route('/transcripts', methods=['POST'])
def get_transcripts():
    """Fetch filtered transcripts based on timestamps."""
    print('ENTRREEEEEIIII')
    try:
        data = request.get_json()
        start_timestamp = data.get('start')
        end_timestamp = data.get('end')
    except (json.JSONDecodeError, TypeError):
        return jsonify({"error": "Invalid JSON data"}), 400

    parsed_start = datetime.strptime(start_timestamp, "[%Y-%m-%d %H:%M:%S]")
    file_name = f"backend/transcription_{parsed_start.strftime('%Y-%m-%d')}.txt"
    print(file_name)
    transcripts = load_data(file_name)

    print(transcripts)

    if start_timestamp:
        try:
            start_timestamp = datetime.strptime(start_timestamp, "[%Y-%m-%d %H:%M:%S]")
        except ValueError:
            return jsonify({"error": "Invalid start timestamp format"}), 400

    if end_timestamp:
        try:
            end_timestamp = datetime.strptime(end_timestamp, "[%Y-%m-%d %H:%M:%S]")
        except ValueError:
            return jsonify({"error": "Invalid end timestamp format"}), 400

    filtered_data = []
    for line in transcripts:
        try:
            timestamp_str, transcript_text = line.split(']', 1)
            timestamp_str = timestamp_str + ']'
            entry_timestamp = datetime.strptime(timestamp_str, "[%Y-%m-%d %H:%M:%S]")
            if (not start_timestamp or entry_timestamp >= start_timestamp) and (not end_timestamp or entry_timestamp <= end_timestamp):
                filtered_data.append(line.strip())
            if len(filtered_data) >= 1000:
                break
        except (ValueError, IndexError):
            continue

    return jsonify(filtered_data)

@app.route('/summaries/<int:user_id>', methods=['GET'])
def get_user_summaries(user_id):
    """Get summaries for a user ordered by creation date."""
    try:
        print(f"Fetching summaries for user ID: {user_id}")
        
        db_manager = DatabaseManager(
            db_name='defaultdb',
            user='avnadmin',
            password='AVNS_U-c1ezivY9TcPqqXrwg',
            host='mysql-3ed7264d-execcsgo-bef4.f.aivencloud.com',
            port=18173
        )
        
        summaries = db_manager.get_summary(user_id)
        print(summaries)

        if not summaries:
            return jsonify({"error": "No summaries found for this user"}), 404

        # Format the response, access columns by key name
        summaries_response = [
            {"id": summary['id'], "summary_text": summary['summary_text'], "user_id": summary['userId']}
            for summary in summaries
        ]

        return jsonify({"summaries": summaries_response}), 200

    except Exception as e:
        print(f"Error: {e}")  # Log the error message
        return jsonify({"error": "An internal error occurred"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5111)
