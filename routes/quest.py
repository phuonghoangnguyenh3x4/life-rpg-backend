from flask import Blueprint, request, jsonify
from utils.auth_utils import token_required, get_player_id_by_token
from wrappers.check_authorized_quest import check_authorized_quest
import json
from utils.factory import createQuestController, createDBHelper

quest_bp = Blueprint('quest', __name__)
questController = createQuestController()
dbHelper = createDBHelper()

@quest_bp.route('/get-quest')
@token_required
def get_quest():
    token = request.cookies.get('auth_token')
    res = get_player_id_by_token(token)
    if res.status_code != 200:
        return res
    id = json.loads(res.data)['id']
    res = questController.get_quest_by_player(request, id)
    return res

@quest_bp.route('/create-quest', methods=["POST"])
@token_required
def create_quest():
    token = request.cookies.get('auth_token')
    res = get_player_id_by_token(token)
    if res.status_code != 200:
        return res
    player_id = json.loads(res.data)['id']
    return questController.create_quest(request, player_id)

@quest_bp.route('/update-quest', methods=["POST"])
@token_required
@check_authorized_quest
def update_quest():
    return questController.update_quest(request)

@quest_bp.route('/delete-quest', methods=["POST"])
@token_required
@check_authorized_quest
def delete_quest():
    return questController.delete_quest(request)
    
@quest_bp.route('/change-quest-status', methods=["POST"])
@token_required
@check_authorized_quest
def change_quest_status():
    return questController.change_status(request)

@quest_bp.route('/change-quest-ord', methods=["POST"])
@token_required
@check_authorized_quest
def change_quest_ord():
    return questController.change_ord(request)

@quest_bp.route('/get-quests')
def get_quests():
    db = dbHelper.get_db()
    return jsonify(list(db["Quest"].rows))