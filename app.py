from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import bcrypt
import os
from functools import wraps
import random
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user_auth_db']
users_collection = db['users']
classrooms_collection = db['classrooms']

# Create indexes
users_collection.create_index("username", unique=True)
classrooms_collection.create_index("code", unique=True)

# Generate unique classroom code
def generate_classroom_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not classrooms_collection.find_one({'code': code}):
            return code

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login first')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'role': role
        }
        
        users_collection.insert_one(user_data)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username})
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            session['role'] = user['role']
            
            if user['role'] == 'teacher' and not user.get('classroom_code'):
                classroom_code = generate_classroom_code()
                
                users_collection.update_one(
                    {'username': username},
                    {'$set': {'classroom_code': classroom_code}}
                )
                
                classrooms_collection.insert_one({
                    'code': classroom_code,
                    'teacher': username,
                    'students': []
                })
                
            flash(f'Welcome back, {username}!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = users_collection.find_one({'username': session['username']})
    if user['role'] == 'teacher':
        classroom = classrooms_collection.find_one({'teacher': session['username']})
        return render_template('dashboard.html', user=user, classroom=classroom)
    else:
        joined_classrooms = list(classrooms_collection.find(
            {'students': session['username']}
        ))
        return render_template('dashboard.html', user=user, joined_classrooms=joined_classrooms)

@app.route('/join_classroom', methods=['GET', 'POST'])
@login_required
def join_classroom():
    if session['role'] != 'student':
        flash('Only students can join classrooms')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        code = request.form['classroom_code']
        classroom = classrooms_collection.find_one({'code': code})
        
        if not classroom:
            flash('Invalid classroom code')
            return redirect(url_for('join_classroom'))
        
        if session['username'] in classroom['students']:
            flash('You are already in this classroom')
            return redirect(url_for('dashboard'))
        
        classrooms_collection.update_one(
            {'code': code},
            {'$push': {'students': session['username']}}
        )
        
        flash('Successfully joined classroom!')
        return redirect(url_for('dashboard'))
    
    return render_template('join_classroom.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
