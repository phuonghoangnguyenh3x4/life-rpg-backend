from flask import Blueprint, request
from utils.auth_utils import token_required, get_player_id_by_token
import json
from utils.factory import createHeatmapController, createDBHelper

heatmap_bp = Blueprint('heatmap', __name__)
heatmapController = createHeatmapController()
dbHelper = createDBHelper()

@heatmap_bp.route('/get-heatmap')
@token_required
def get_heatmap():
    token = request.cookies.get('auth_token')
    res = get_player_id_by_token(token)
    if res.status_code != 200:
        return res
    id = json.loads(res.data)['id']
    res = heatmapController.get_heatmap_by_player(id)
    return res