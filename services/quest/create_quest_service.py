from flask import make_response
from utils.randint import randint
from utils.quest_utils import get_exp_from_difficulty, get_money_from_difficulty
from flask import jsonify
from services.quest.get_quest_service import GetQuestService
from enums.quest_status import QuestStatus
import json
from services.player.update_player_service import UpdatePlayerService
class CreateQuestService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._get_quest_service = GetQuestService(dbHelper)
        self._update_player_service = UpdatePlayerService(dbHelper)

    def create_quest(self, request, player_id):
        db = self._dbHelper.get_db()
        name = request.form.get('name')
        status = request.form.get('status')
        difficulty = request.form.get('difficulty')
        ord = request.form.get('ord')
        note = request.form.get('note')
        seed = randint.get()
        exp = get_exp_from_difficulty(difficulty, seed)
        money = get_money_from_difficulty(difficulty, seed)

        if not name or not status or not difficulty:
            return jsonify({'error': 'Name, status, difficulty are required'}), 400
        player_id = int(player_id)
        questTable = db['Quest'].insert({
            'name': name,
            'status': status,
            'difficulty': difficulty,
            'seed': seed,
            'exp': exp,
            'money': money,
            'ord': ord,
            'player_id': player_id,
            'note': note
        })
        res = self._get_quest_service._get_by_id(questTable.last_rowid)
        self.__update_stat_quest_done(status, res)
        return make_response(res, 200)
    
    def __update_stat_quest_done(self, status, get_quest_service_res):
        if status != QuestStatus.Done:
            return

        res = get_quest_service_res
        if res.status_code != 200:
            return res
        quest = json.loads(res.data)
        res = self._update_player_service.update_stat_quest_done(quest)
    