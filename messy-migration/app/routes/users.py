from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.validators import validate_user_input
import sqlite3

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.get_all()
    return jsonify(users), 200


@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    valid, error = validate_user_input(data, required_fields=["name", "email", "password"])
    if not valid:
        return jsonify({"error": error}), 400

    try:
        user_id = User.create(data["name"], data["email"], data["password"])
        return jsonify({"message": "User created", "user_id": user_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409


@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    valid, error = validate_user_input(data, required_fields=["name", "email"])
    if not valid:
        return jsonify({"error": error}), 400

    updated = User.update(user_id, data["name"], data["email"])
    if updated:
        return jsonify({"message": "User updated"}), 200
    return jsonify({"error": "User not found"}), 404


@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleted = User.delete(user_id)
    if deleted:
        return jsonify({"message": f"User {user_id} deleted"}), 200
    return jsonify({"error": "User not found"}), 404


@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Missing search query: name"}), 400

    try:
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
            users = cursor.fetchall()
            return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
