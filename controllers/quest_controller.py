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
        
    def get_quest_by_player(self, player_id):
        try:
            db = self.dbHelper.get_db()
            quests = db["Quest"].rows_where(f"player_id = ?", [player_id])
            return make_response(list(quests), 200)
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