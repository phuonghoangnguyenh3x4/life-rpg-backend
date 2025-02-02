from flask import jsonify
from sqlite_utils.utils import sqlite3
import logging
from flask import make_response
import random

class QuestController:
    difficulty_exp_map = {
        "Trivial": (0, 20),
        "Easy": (20, 100),
        "Normal": (100, 200),
        "Hard": (200, 300),
        "SuperHard": (450, 550)   
    }
    
    def __init__(self, dbHelper):
        self.dbHelper = dbHelper
    
    def get_typed_quests(self, player_id, type, limit, offset): 
        db = self.dbHelper.get_db()
        quests = db["Quest"].rows_where(f"player_id = ? and status = ?", [player_id, type], order_by="id desc", limit=limit, offset=offset)
        return list(quests)
    
    def get_typed_quests_count(self, player_id, type):
        db = self.dbHelper.get_db()
        count = db["Quest"].count_where("player_id = ? and status = ?", [player_id, type]) 
        return count
        
    def get_3_typed_quests(self, player_id, limit, offset):
        todos = self.get_typed_quests(player_id, "Todo", limit, offset)
        doings = self.get_typed_quests(player_id, "Doing", limit, offset)
        dones = self.get_typed_quests(player_id, "Done", limit, offset)
        return [*todos, *doings, *dones]
        
    def get_max_count_3_typed_quests(self, player_id):
        todos_count = self.get_typed_quests_count(player_id, "Todo")
        doings_count = self.get_typed_quests_count(player_id, "Doing")
        dones_count = self.get_typed_quests_count(player_id, "Done")
        return max(todos_count, doings_count, dones_count)
    
    def get_quest_by_player(self, request, player_id):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            limit = per_page
            offset = (page - 1) * per_page

            db = self.dbHelper.get_db()
            total_quests = self.get_max_count_3_typed_quests(player_id)
            quests = self.get_3_typed_quests(player_id, limit, offset)
            
            data = {
                'total': total_quests,
                'pages': (total_quests + per_page - 1) // per_page,
                'current_page': page,
                'per_page': per_page,
                'quests': list(quests)
            }
            return make_response(data, 200)
        except Exception as e:
            logging.exception(e)
            return make_response('Can not find quests', 404)
        
    def get_player_id(self, request):
        try:
            quest_id = request.form.get('id')
            db = self.dbHelper.get_db()
            res = db["Quest"].rows_where(f"id = ?", [quest_id], select="player_id")
            quest = list(res)[0]
            return make_response(quest, 200)
        except Exception as e:
            logging.exception(e)
            return make_response('Can not find quest', 404)
    
    def create_quest(self, request):
        try:
            db = self.dbHelper.get_db()
            name = request.form.get('name')
            status = request.form.get('status')
            difficulty = request.form.get('difficulty')
            player_id = request.form.get('playerId')
            exp = self.__get_exp_from_difficulty(difficulty)
            money = self.__get_money_from_difficulty(difficulty)

            if not name or not status or not difficulty or not player_id:
                return jsonify({'error': 'Name, status, difficulty and playerId are required'}), 400
            player_id = int(player_id)
            print(player_id)
            db['Quest'].insert({
                'name': name,
                'status': status,
                'difficulty': difficulty,
                'exp': exp,
                'money': money,
                'player_id': player_id
            })
            return make_response('Quest created successfully', 200)
        except sqlite3.IntegrityError:
            logging.exception(sqlite3.IntegrityError)
            return make_response('User not existed', 400)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
    
    def change_status(self, request):
        try:
            db = self.dbHelper.get_db()
            id = request.form.get('id')
            new_status = request.form.get('status')
            
            db["Quest"].update(id, {"status": new_status})
            return make_response('Status updated successfully', 200)
        except sqlite3.IntegrityError:
            logging.exception(sqlite3.IntegrityError)
            return make_response('Status not existed', 400)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
        
    def change_difficulty(self, request):
        try:
            db = self.dbHelper.get_db()
            id = request.form.get('id')
            difficulty = request.form.get('difficulty')
            
            db["Quest"].update(id, {"difficulty": difficulty})
            return make_response('Difficulty updated successfully', 200)
        except sqlite3.IntegrityError:
            logging.exception(sqlite3.IntegrityError)
            return make_response('Difficulty not existed', 400)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
    
    def __get_exp_from_difficulty(self, difficulty):
        return random.randint(*QuestController.difficulty_exp_map[difficulty])
    
    def __get_money_from_difficulty(self, difficulty):
        return self.__get_exp_from_difficulty(difficulty)*2