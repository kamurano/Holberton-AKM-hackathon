from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_swagger_ui import get_swaggerui_blueprint
from itsdangerous import URLSafeTimedSerializer
import smtplib
import random
from email.mime.text import MIMEText

from controller.auth import auth_controller
from controller.user import user_controller
from secret.jwt import jwt_secret

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = jwt_secret

jwt = JWTManager(app)


SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)


app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(auth_controller)
app.register_blueprint(user_controller)


@app.route('/')
@jwt_required()
def home():
    return jsonify({"message": "Hello, World!"})

app.run(port=5000, debug=True)