from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer

from repository.user import UserRepository
from utils.mail import send_email, send_verification_email
from secret.jwt import jwt_secret



admin_controller = Blueprint('user_controller', __name__)

admin_repository = UserRepository()

@admin_controller.route('/change_admin_status/<user_id>', methods=['GET'])
@jwt_required()
def change_admin_status(user_id):
    current_user = get_jwt_identity()
    if current_user.get('is_admin') == False:
        return jsonify({"message": "Admin access required"}), 403
    
    valid, user = admin_repository.get_user(user_id)
    if not valid:
        return jsonify(user), 400
    
    if user['users_is_admin'] == 1:
        admin_repository.update_admin_status(user_id, 0)
        return jsonify({"message": "User is no longer an admin"}), 200
    admin_repository.update_admin_status(user_id, 1)
    return jsonify({"message": "User is now an admin"}), 200