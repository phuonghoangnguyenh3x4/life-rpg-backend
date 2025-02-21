from flask import make_response
import json
from services.player.update_player_service import UpdatePlayerService
from services.quest.get_quest_service import GetQuestService
from enums.quest_status import QuestStatus

class DeleteQuestService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._update_player_service = UpdatePlayerService(dbHelper)
        self._get_quest_service = GetQuestService(dbHelper)

    def delete_quest(self, request):
        db = self._dbHelper.get_db()
        id = request.form.get('id')
        res = self._get_quest_service._get_by_id(id)
        self.__update_stat_quest_undone(res)
        db["Quest"].delete(id)
        return make_response('Delete quest successfully', 200)
    
    def __update_stat_quest_undone(self, get_quest_service_res):
        res = get_quest_service_res
        if res.status_code != 200:
            return res
        quest = json.loads(res.data)
        if quest['status'] != QuestStatus.Done:
            return
        res = self._update_player_service.update_stat_quest_undone(quest)