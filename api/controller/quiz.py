from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer

from repository.quiz import QuizRepository
from utils.mail import send_email, send_verification_email
from secret.jwt import jwt_secret



quiz_controller = Blueprint('quiz_controller', __name__)

quiz_repository = QuizRepository()

@quiz_controller.route('/quiz', methods=['POST'])
@jwt_required()
def create_quiz():
    current_user = get_jwt_identity()
    if current_user['is_admin'] != True:
        return jsonify({"message": "Unauthorized"}), 401
    
    avg_score = 0
    title = request.json['title']
    questions = request.json['questions']
    question_description = request.json['question_description']
    answers = request.json['answers']
    correct_answers = request.json['correct_answers']
    stars = 0

    valid, response = quiz_repository.create(avg_score, title, questions, question_description, answers, correct_answers, stars)
    if not valid:
        return jsonify(response), 400
    return jsonify(response), 200


@quiz_controller.route('/quizes', methods=['GET'])
@jwt_required()
def get_all_quizzes():
    current_user = get_jwt_identity()
    if current_user['is_admin'] != True:
        return jsonify({"message": "Unauthorized"}), 401

    quizzes = quiz_repository.get_all()
    return jsonify(quizzes), 200