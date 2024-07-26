import re


class UserService:

    @staticmethod
    def validate_user(fname, sname, email, password, password_confirmation):
        if not email:
            return False, {"message": "Missing username"}
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, {"message": "Invalid email address"}
        if not fname:
            return False, {"message": "Missing first name"}
        if not sname:
            return False, {"message": "Missing second name"}
        if not password:
            return False, {"message": "Missing password"}
        if not password_confirmation:
            return False, {"message": "Missing password confirmation"}
        if password != password_confirmation:
            return False, {"message": "Passwords do not match"}
        if len(password) < 8:
            return False, {"message": "Password is too short"}
        if len(password) > 50:
            return False, {"message": "Password is too long"}
        return True, None
    
    @staticmethod
    def validate_login(email, password):
        if not email:
            return False, {"message": "Missing email"}
        if not password:
            return False, {"message": "Missing password"}
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, {"message": "Invalid email address"}
        return True, None