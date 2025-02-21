from flask import make_response
from utils.randint import randint
from utils.quest_utils import get_exp_from_difficulty, get_money_from_difficulty
from services.quest.get_quest_service import GetQuestService
from services.player.update_player_service import UpdatePlayerService
import json
from enums.quest_status import QuestStatus
class UpdateQuestService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._get_quest_service = GetQuestService(dbHelper)
        self._update_player_service = UpdatePlayerService(dbHelper)

    def update_quest(self, request):
        id = request.form.get('id')
        name = request.form.get('name')
        difficulty = request.form.get('difficulty')
        note = request.form.get('note')

        res = self._get_quest_service._get_by_id(id)
        if res.status_code != 200:
            return res
        quest = json.loads(res.data)
        seed = quest['seed']
        if seed == None:
            seed = randint.get()
        exp = get_exp_from_difficulty(difficulty, seed)
        money = get_money_from_difficulty(difficulty, seed)

        db = self._dbHelper.get_db()
        db["Quest"].update(id, {"name": name,
                                "difficulty": difficulty,
                                "seed": seed,
                                "exp": exp,
                                "money": money,
                                "note": note})
        
        updated_quest = self._get_quest_service._get_by_id(id)
        return make_response(updated_quest, 200)
    
    def change_status(self, request):
        db = self._dbHelper.get_db()
        id = request.form.get('id')
        new_status = request.form.get('status')
        
        res = self._get_quest_service._get_by_id(id)
        if res.status_code != 200:
            return res
        quest = json.loads(res.data)
        old_status = quest['status']

        if old_status != QuestStatus.Done and new_status == QuestStatus.Done:
            res = self._update_player_service.update_stat_quest_done(quest)
            if res.status_code != 200:
                return res
        
        if old_status == QuestStatus.Done and new_status != QuestStatus.Done:
            res = self._update_player_service.update_stat_quest_undone(quest)
            if res.status_code != 200:
                return res
                
        db["Quest"].update(id, {"status": new_status})
        return make_response('Status updated successfully', 200)
    
    def change_ord(self, request):
        db = self._dbHelper.get_db()
        id = request.form.get('id')
        ord = request.form.get('ord')
        
        db["Quest"].update(id, {"ord": ord})
        return make_response('Order updated successfully', 200)
    