from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from repository.user import UserRepository
from service.user import UserService

auth_controller = Blueprint('auth_controller', __name__)


user_repository = UserRepository()

@auth_controller.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email", None)
    fname = request.json.get("fname", None)
    sname = request.json.get("sname", None)
    password = request.json.get("password", None)
    password_confirmation = request.json.get("password_confirmation", None)
    valid, message = UserService.validate_user(fname, sname, email, password, password_confirmation)
    if not valid:
        return jsonify(message), 400
    valid, message = user_repository.create(fname, sname, email, generate_password_hash(password))
    if not valid:
        return jsonify(message), 400
    return jsonify({"message": "User created"}), 201  
    

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    valid, user = user_repository.get(email)
    if not valid:
        return jsonify(user), 400
    if user and check_password_hash(user['users_password'], password):
        access_token = create_access_token(identity={'email': email}, expires_delta=timedelta(days=7))
        return jsonify({"message": "Logged in successfully", "access_token": access_token}), 200
    return jsonify({"message": "Invalid email or password"}), 400