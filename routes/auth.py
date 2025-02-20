from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required
from models.user import User
from app import mongo

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")  # "teacher" or "student"

        # Check if email already exists
        if mongo.db.users.find_one({"email": email}):
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.signup"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "role": role,
            "classroom_code": None
        }
        mongo.db.users.insert_one(user_data)

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user_data = mongo.db.users.find_one({"email": email})
        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            session["role"] = user.role
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid credentials.", "danger")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
