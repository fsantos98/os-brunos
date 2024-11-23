from flask import Flask, request, jsonify
from datetime import datetime
import json

# Assuming DatabaseManager is defined in a separate file, e.g., `database.py`
from sqlite import DatabaseManager  # Adjust the import path if necessary

app = Flask(__name__)

def load_data(file_name):
    """Load transcript data from a file."""
    try:
        with open(file_name, "r") as f:
            return f.readlines()
    except FileNotFoundError:
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

    db_manager = DatabaseManager()
    user = db_manager.get_user_by_email(email)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Assuming the user tuple structure: (id, name, email, password)
    if user[3] != password:
        return jsonify({"error": "Invalid password"}), 400

    return jsonify({"success": "Authentication successful"}), 200

@app.route('/transcripts', methods=['POST'])
def get_transcripts():
    """Fetch filtered transcripts based on timestamps."""
    try:
        data = request.get_json()
        start_timestamp = data.get('start')
        end_timestamp = data.get('end')
    except (json.JSONDecodeError, TypeError):
        return jsonify({"error": "Invalid JSON data"}), 400

    file_name = f"transcription_{datetime.now().strftime('%Y-%m-%d')}.txt"
    transcripts = load_data(file_name)

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

if __name__ == '__main__':
    app.run(debug=True, port=5111)
