from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer

from repository.user import UserRepository
from utils.mail import send_email, send_verification_email
from secret.jwt import jwt_secret



user_controller = Blueprint('user_controller', __name__)

user_repository = UserRepository()


@user_controller.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if current_user.get('is_admin') == False:
        return jsonify({"message": "Admin access required"}), 403
    
    users = user_repository.get_users()
    return jsonify(users), 200

@user_controller.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    
    print(current_user)
    valid, user = user_repository.get_user(user_id)
    if not valid:
        return jsonify(user), 400
    
    if current_user.get('is_admin') == True:
        return jsonify(user)
    
    if current_user.get('id') != user['users_id']:
        return jsonify ({"message": "Unauthorized"}), 403
    
    return jsonify(user), 200

@user_controller.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    print(current_user)
    if current_user.get('is_admin') == True or current_user.get('id') == user_id:
        valid, user = user_repository.get_user(user_id)
        if not valid:
            return jsonify(user), 400
        
        data = request.get_json()
        fname = data.get('fname', user['users_fname'])
        sname = data.get('sname', user['users_sname'])
        
        valid, message = user_repository.update_user_by_id(user_id, fname, sname)
        if not valid:
            return jsonify(message), 400
        
        return jsonify({"message": "User updated"}), 200
    return jsonify({"message": "Admin access required"}), 403


@user_controller.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    
    if current_user.get('is_admin') == False:
        return jsonify({"message": "Admin access required"}), 403
    
    valid, user = user_repository.get_user(user_id)
    if not valid:
        return jsonify(user), 400
    
    user_repository.delete_user(user_id)
    return jsonify({"message": "User deleted"}), 200