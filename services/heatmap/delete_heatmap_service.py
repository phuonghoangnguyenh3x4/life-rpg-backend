from flask import make_response
from services.player.update_player_service import UpdatePlayerService
from services.quest.get_quest_service import GetQuestService
import datetime
from utils.db_utils import DBHelper

class DeleteHeatmapService:
    def __init__(self, dbHelper: DBHelper):
        self._dbHelper = dbHelper

    def delete_heatmap(self, date: datetime.date, player_id):
        db = self._dbHelper.get_db()
        db["Heatmap"].delete((date, player_id))
        return make_response('Delete heatmap successfully', 200)