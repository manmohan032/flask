from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.validators import validate_user_input

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    valid, error = validate_user_input(data, required_fields=["email", "password"])
    if not valid:
        return jsonify({"error": error}), 400

    user_id = User.check_password(data["email"], data["password"])
    if user_id:
        return jsonify({"status": "success", "user_id": user_id}), 200
    else:
        return jsonify({"status": "failed", "error": "Invalid credentials"}), 401
