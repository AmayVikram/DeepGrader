from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  # Required for session management

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"  # Redirect to login if unauthorized

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

from routes.auth import auth
app.register_blueprint(auth, url_prefix="/auth")

if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:5000/")
    app.run(debug=True)


