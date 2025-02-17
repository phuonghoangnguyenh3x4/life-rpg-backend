from flask import Blueprint, request, make_response, jsonify
from utils.auth_utils import token_required, decode_token
import json
from utils.factory import createPlayerController, createDBHelper

player_bp = Blueprint('player', __name__)
playerController = createPlayerController()
dbHelper = createDBHelper()

@player_bp.route('/get-player')
@token_required
def get_player():
    token = request.cookies.get('auth_token')
    res = decode_token(token)
    if res.status_code != 200:
        return make_response('Invalid token', 401)
    
    json_string = res.data.decode('utf-8')
    token_dict = json.loads(json_string)
    email = token_dict['username']
    res = playerController.get_player_by_email(email)
    return res

@player_bp.route('/get-users')
def get_users():
    db = dbHelper.get_db()
    return jsonify(list(db["Player"].rows))