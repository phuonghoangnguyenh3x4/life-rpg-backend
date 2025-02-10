from dotenv import load_dotenv
from flask_cors import CORS
import os
from helpers.db_helper import DBHelper
from controllers.player_controller import PlayerController
from controllers.quest_controller import QuestController
from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps
import base64
import json

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
        return make_response(payload, 200)
    except jwt.ExpiredSignatureError:
        return make_response('Token has expired', 401)
    except jwt.InvalidTokenError:
        return make_response('Invalid token', 401)
    
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

def check_authorized_quest(f): 
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        res = get_player_id_by_token(token)
        if res.status_code != 200:
            return res
        player_id_1 = json.loads(res.data)['id']
        questController = QuestController(dbHelper)
        res = questController.get_player_id(request)
        if res.status_code != 200:
            return res
        player_id_2 = json.loads(res.data)['player_id']
        if player_id_1 != player_id_2:
            return make_response('Unauthorized', 401)
        return f(*args, **kwargs)
    return decorated


@app.route('/create-account', methods=["POST"])
def create_account():
    playerController = PlayerController(dbHelper)
    res = playerController.create_account(request)
    email = request.form.get('email')
    if res.status_code == 201:
        token = generate_token(email)
        res.set_cookie('auth_token', token, httponly=True, secure=True, samesite='none')
    return res

@app.route('/login', methods=["POST"])
def login():
    playerController = PlayerController(dbHelper)
    res = playerController.login(request)
    email = request.form.get('email')
    if res.status_code == 202:
        token = generate_token(email)
        res.set_cookie('auth_token', token, httponly=True, secure=True, samesite='none')
    return res

@app.route('/logout', methods=["POST"])
@token_required
def logout():
    res = make_response('Logout successful')
    res.set_cookie('auth_token', '', httponly=True, secure=True, samesite='none', expires=0)
    return res

@app.route('/get-player')
@token_required
def get_player():
    token = request.cookies.get('auth_token')
    res = decode_token(token)
    if res.status_code != 200:
        return make_response('Invalid token', 401)
    
    json_string = res.data.decode('utf-8')
    token_dict = json.loads(json_string)
    email = token_dict['username']
    playerController = PlayerController(dbHelper)
    res = playerController.get_player_by_email(email)
    return res

def get_player_id_by_token(token):
    token = request.cookies.get('auth_token')
    res = decode_token(token)
    if res.status_code != 200:
        return make_response('Invalid token', 401)
    
    json_string = res.data.decode('utf-8')
    token_dict = json.loads(json_string)
    email = token_dict['username']
    playerController = PlayerController(dbHelper)
    return playerController.get_id_by_email(email)

@app.route('/get-quest')
@token_required
def get_quest():
    token = request.cookies.get('auth_token')
    res = get_player_id_by_token(token)
    if res.status_code != 200:
        return res
    id = json.loads(res.data)['id']
    questController = QuestController(dbHelper)
    res = questController.get_quest_by_player(request, id)
    print(res)
    return res

@app.route('/create-quest', methods=["POST"])
@token_required
def create_quest():
    token = request.cookies.get('auth_token')
    res = get_player_id_by_token(token)
    if res.status_code != 200:
        return res
    player_id = json.loads(res.data)['id']
    questController = QuestController(dbHelper)
    res = questController.create_quest(request, player_id)
    return res
    
@app.route('/change-quest-status', methods=["POST"])
@token_required
@check_authorized_quest
def change_quest_status():
    questController = QuestController(dbHelper)
    res = questController.change_status(request)
    return res

@app.route('/change-quest-ord', methods=["POST"])
@token_required
@check_authorized_quest
def change_quest_ord():
    questController = QuestController(dbHelper)
    res = questController.change_ord(request)
    return res

@app.route('/change-quest-difficulty', methods=["POST"])
@token_required
@check_authorized_quest
def change_quest_difficulty():
    questController = QuestController(dbHelper)
    res = questController.change_difficulty(request)
    return res

@app.route('/get-users')
def get_users():
    db = dbHelper.get_db()
    players = db["Player"].rows
    return list(players)

@app.route('/get-quests')
def get_quests():
    db = dbHelper.get_db()
    quests = db["Quest"].rows
    return list(quests)

# Protected endpoint for test
@app.route('/check-auth')
@token_required
def check_auth():
    return 'This is a check auth route'

if __name__ == '__main__':
    app.run(debug=True)
