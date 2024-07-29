from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer

from repository.user import UserRepository
from service.user import UserService
from utils.mail import send_email, send_verification_email, send_phishing_mail
from secret.jwt import jwt_secret

auth_controller = Blueprint('auth_controller', __name__)

serializer = URLSafeTimedSerializer(jwt_secret)

user_repository = UserRepository()

otp_store = {}

@auth_controller.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email", None)
    fname = request.json.get("fname", None).capitalize()
    sname = request.json.get("sname", None).capitalize()
    password = request.json.get("password", None)
    password_confirmation = request.json.get("password_confirmation", None)
    
    valid, message = UserService.validate_user(fname, sname, email, password, password_confirmation)
    if not valid:
        return jsonify(message), 400
    
    valid, message = user_repository.create(fname, sname, email, generate_password_hash(password))
    if not valid:
        return jsonify(message), 400
    
    # Generate verification token
    token = serializer.dumps(email, salt='email-confirm-salt')
    # Send verification email
    send_verification_email(email, token)
    
    # send_phishing_mail(email)
    send_email(email, "Verify Email", "Please click the link to verify your email : http://localhost:5000/linkedin")
    return jsonify({"message": "User created. Please verify your email with the link sent."}), 201  
    

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    valid, user = user_repository.get(email)
    if not valid:
        return jsonify(user), 400
    
    valid, message = UserService.validate_login(email, password)
    if not valid:
        return jsonify(message), 400
    
    valid, message = user_repository.get_user_active_status(email)
    if not valid:
        # Generate verification token
        token = serializer.dumps(email, salt='email-confirm-salt')
        # Send verification email
        send_verification_email(email, token)
        return jsonify(message), 400
    
    if user and check_password_hash(user['users_password'], password):
        access_token = create_access_token(identity={"id": user["users_id"], 'email': email, "is_admin": user["users_is_admin"]}, expires_delta=timedelta(days=7))
        return jsonify({"message": "Logged in successfully", "access_token": access_token}), 200
    return jsonify({"message": "Invalid email or password"}), 400   


@auth_controller.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=3600)
        
        valid, message = user_repository.activate_user(email)
        if not valid:
            return jsonify(message), 400

        return jsonify({"message": "Email verified successfully."}), 200
    except Exception as e:
        return jsonify({"message": "Invalid or expired token."}), 400