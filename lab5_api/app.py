"""Lab 5 Flask REST API for managing users."""
from flask import Flask, jsonify, request
from flask_cors import CORS
try:
    from .database import create_db_table, get_users, get_user_by_id, insert_user, update_user, delete_user, FIELDS
except ImportError:
    from database import create_db_table, get_users, get_user_by_id, insert_user, update_user, delete_user, FIELDS

app = Flask(__name__)
CORS(app)
create_db_table()

def read_user_payload(updating=False):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, (jsonify({"error": "Provide a JSON object"}), 400)
    missing = [field for field in FIELDS if not isinstance(data.get(field), str) or not data[field].strip()]
    if missing:
        return None, (jsonify({"error": "Missing or empty fields", "fields": missing}), 400)
    if updating:
        if isinstance(data.get("user_id"), bool) or not isinstance(data.get("user_id"), int) or data["user_id"] < 1:
            return None, (jsonify({"error": "user_id must be a positive integer"}), 400)
    return data, None

@app.get('/api/users')
def api_get_users():
    return jsonify(get_users())

@app.get('/api/users/<int:user_id>')
def api_get_user(user_id):
    user = get_user_by_id(user_id)
    return (jsonify(user), 200) if user else (jsonify({"error": "User not found"}), 404)

@app.post('/api/users/add')
def api_add_user():
    data, error = read_user_payload()
    if error:
        return error
    return jsonify(insert_user(data)), 201

@app.put('/api/users/update')
def api_update_user():
    data, error = read_user_payload(updating=True)
    if error:
        return error
    user = update_user(data)
    return (jsonify(user), 200) if user else (jsonify({"error": "User not found"}), 404)

@app.delete('/api/users/delete/<int:user_id>')
def api_delete_user(user_id):
    if not delete_user(user_id):
        return jsonify({"error": "User not found"}), 404
    return jsonify({"status": "User deleted successfully"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
