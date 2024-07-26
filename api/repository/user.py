from model.user import UserModel

class UserRepository:
    def __init__(self):
        self.user_model = UserModel()
    
    def get(self, user_email):
        user = self.user_model.get_record_by_email("users", user_email)
        if not user:
            return False, {"message": "User not found"}
        return True, user
    
    def get_all(self):
        return self.user_model.get_all_records("users")
    
    def create(self, fname, sname, email, password, is_admin=False):
        if email in [user['users_email'] for user in self.get_all()]:
            return False, {"message": "User already exists"}
        self.user_model.insert("users", fname, sname, email, password, is_admin)
        return True, {"message": "User created"}
    
    def activate_user(self, user_email):
        user = self.user_model.get_record_by_email("users", user_email)
        if not user:
            return False, {"message": "User not found"}
        if user['users_is_active']:
            return False, {"message": "User already active"}
        self.user_model.activate_email("users", user_email)
        return True, {"message": "User activated"}
    
    def get_user_active_status(self, user_email):
        user = self.user_model.get_user_active_status("users", user_email)
        if not user:
            return False, {"message": "User not found"}
        if not user['users_is_active']:
            return False, {"message": "User not active"}
        return True, user