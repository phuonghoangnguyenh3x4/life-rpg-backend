from functools import wraps
from flask import request, make_response
import json
from utils.auth_utils import get_player_id_by_token
from utils.factory import createGetQuestService

def check_authorized_quest(f): 
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        res = get_player_id_by_token(token)
        if res.status_code != 200:
            return res
        player_id_1 = json.loads(res.data)['id']

        get_quest_service = createGetQuestService()
        res = get_quest_service.get_player_id(request)
        if res.status_code != 200:
            return res
        player_id_2 = json.loads(res.data)['player_id']
        if player_id_1 != player_id_2:
            return make_response('Unauthorized', 401)
        return f(*args, **kwargs)
    return decorated