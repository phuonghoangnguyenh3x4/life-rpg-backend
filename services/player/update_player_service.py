from flask import make_response
import json
from helpers.config import exp_2_lv_up
from services.player.get_player_service import GetPlayerService

class UpdatePlayerService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._get_player_service = GetPlayerService(dbHelper)

    def update_stat_quest_done(self, quest):
        res = self._get_player_service.get_by_id(quest['player_id'])
        if res.status_code != 200:
            return res
        player = json.loads(res.data)

        money = player['money'] + quest['money']
        exp = player['exp'] + quest['exp']
        lv = exp//exp_2_lv_up
        progress = (exp % exp_2_lv_up) * 100 / exp_2_lv_up
        progress = round(progress, 2)
        
        db = self._dbHelper.get_db()
        db["Player"].update(quest['player_id'], 
                            {"level": lv, "exp": exp, 
                            "money": money, "progress": progress})

        return make_response('Player stat update successfully', 200)
    
    def update_stat_quest_undone(self, quest):
        res = self._get_player_service.get_by_id(quest['player_id'])
        if res.status_code != 200:
            return res
        player = json.loads(res.data)
        
        money = player['money'] - quest['money']
        exp = player['exp'] - quest['exp']
        lv = exp//exp_2_lv_up
        progress = (exp % exp_2_lv_up) * 100 / exp_2_lv_up
        progress = round(progress, 2)
        
        db = self._dbHelper.get_db()
        db["Player"].update(quest['player_id'], 
                            {"level": lv, "exp": exp, 
                            "money": money, "progress": progress})

        return make_response('Player stat update successfully', 200)