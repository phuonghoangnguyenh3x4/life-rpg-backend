from dotenv import load_dotenv
from flask_cors import CORS
import os
from helpers.db_helper import DBHelper
from controllers.player_controller import PlayerController
from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps
import base64

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

dbHelper = DBHelper(DB_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = base64.b64decode(SECRET_KEY)
CORS(app, supports_credentials=True)

def generate_token(username):
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
    
# Verify a token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/create-account', methods=["POST"])
def create_account():
    playerController = PlayerController(dbHelper)
    res = playerController.create_account(request)
    email = request.form.get('email')
    if res[1] == 201:
        token = generate_token(email)
        res = make_response('Account created successfully')
        res.set_cookie('auth_token', token, httponly=True, secure=True, samesite='none')
    return res

@app.route('/login', methods=["POST"])
def login():
    playerController = PlayerController(dbHelper)
    res = playerController.login(request)
    email = request.form.get('email')
    if res[1] == 202:
        token = generate_token(email)
        res = make_response('Login successful')
        res.set_cookie('auth_token', token, httponly=True, secure=True, samesite='none')
    return res

@app.route('/logout', methods=["POST"])
@token_required
def logout():
    res = make_response('Logout successful')
    res.set_cookie('auth_token', '', httponly=True, secure=True, samesite='none', expires=0)
    return res

@app.route('/get-users')
def get_users():
    db = dbHelper.get_db()
    for row in db["Player"].rows:
        print(row)
    return 'ok'

# Protected endpoint for test
@app.route('/check-auth')
@token_required
def check_auth():
    return 'This is a check auth route'

if __name__ == '__main__':
    app.run(debug=True)
