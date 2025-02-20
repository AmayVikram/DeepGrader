from flask_login import UserMixin
from flask_pymongo import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.role = user_data["role"]  # "teacher" or "student"
        self.classroom_code = user_data.get("classroom_code", None)
