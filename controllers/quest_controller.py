import json
from flask import jsonify
from sqlite_utils.utils import sqlite3
import logging
from flask import make_response
import random

from controllers.player_controller import PlayerController
from helpers.randint import randint

class QuestController:
    difficulty_exp_map = {
        "Trivial": (1, 20),
        "Easy": (20, 100),
        "Normal": (100, 200),
        "Hard": (200, 300),
        "SuperHard": (450, 550)   
    }
    
    def __init__(self, dbHelper):
        self.dbHelper = dbHelper
    
    def get_type_quests(self, player_id, type, limit, offset): 
        db = self.dbHelper.get_db()
        quests = db["Quest"].rows_where(f"player_id = ? and status = ?", [player_id, type], order_by="ord desc", limit=limit, offset=offset)
        return list(quests)
    
    def get_type_quests_count(self, player_id, type):
        db = self.dbHelper.get_db()
        count = db["Quest"].count_where("player_id = ? and status = ?", [player_id, type]) 
        return count
        
    def get_3_type_quests(self, player_id, limit, offset):
        todos = self.get_type_quests(player_id, "Todo", limit, offset)
        doings = self.get_type_quests(player_id, "Doing", limit, offset)
        dones = self.get_type_quests(player_id, "Done", limit, offset)
        return [*todos, *doings, *dones]
    
    def get_3_type_count(self, player_id):
        todo = self.get_type_quests_count(player_id, "Todo")
        doing = self.get_type_quests_count(player_id, "Doing")
        done = self.get_type_quests_count(player_id, "Done")
        return {
            'Todo': todo,
            'Doing': doing,
            'Done': done
        }

    def get_prev_page_ord_by_type(self, player_id, page, per_page, type, type_count):
        offset = ((page - 1) * per_page) - 1
        if offset < 0:
            return None
        if type_count <= 0:
            return None
        if offset > type_count:
            offset = type_count - 1
        db = self.dbHelper.get_db()
        quest = db["Quest"].rows_where(f"player_id = ? and status = ?", [player_id, type], order_by="ord desc", limit=1, offset=offset)
        quest = list(quest)
        if len(quest) < 1:
            return None
        quest = quest[0]
        return quest['ord']
    
    def get_next_page_ord_by_type(self, player_id, page, per_page, type, type_count):
        offset = ((page - 1) * per_page) + per_page
        if offset >= type_count:
            return None
        if type_count <= 0:
            return None
        db = self.dbHelper.get_db()
        quest = db["Quest"].rows_where(f"player_id = ? and status = ?", [player_id, type], order_by="ord desc", limit=1, offset=offset)
        quest = list(quest)
        if len(quest) < 1:
            return None
        quest = quest[0]
        return quest['ord']
    
    def get_prev_page_ord(self, player_id, page, per_page, type_counts):
        types = ['Todo', 'Doing', 'Done']
        res = {}
        for type in types:
            ord = self.get_prev_page_ord_by_type(player_id, page, per_page, type, type_counts[type])
            res[type] = ord
        return res
    
    def get_next_page_ord(self, player_id, page, per_page, type_counts):
        types = ['Todo', 'Doing', 'Done']
        res = {}
        for type in types:
            ord = self.get_next_page_ord_by_type(player_id, page, per_page, type, type_counts[type])
            res[type] = ord
        return res
        
    def get_quest_by_player(self, request, player_id):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            limit = per_page
            offset = (page - 1) * per_page

            type_counts = self.get_3_type_count(player_id)
            max_quests = max([v for k,v in type_counts.items()])
            total_quests = sum([v for k,v in type_counts.items()])
            quests = self.get_3_type_quests(player_id, limit, offset)
            prev_ord = self.get_prev_page_ord(player_id, page, per_page, type_counts)
            next_ord = self.get_next_page_ord(player_id, page, per_page, type_counts)
            
            data = {
                'total': total_quests,
                'max_quests': max_quests,
                'pages': (max_quests + per_page - 1) // per_page,
                'current_page': page,
                'per_page': per_page,
                'quests': list(quests),
                'prev_ord': prev_ord,
                'next_ord': next_ord
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
    
    def create_quest(self, request, player_id):
        try:
            db = self.dbHelper.get_db()
            name = request.form.get('name')
            status = request.form.get('status')
            difficulty = request.form.get('difficulty')
            ord = request.form.get('ord')
            note = request.form.get('note')
            seed = randint.get()
            exp = self.__get_exp_from_difficulty(difficulty, seed)
            money = self.__get_money_from_difficulty(difficulty, seed)

            if not name or not status or not difficulty:
                return jsonify({'error': 'Name, status, difficulty are required'}), 400
            player_id = int(player_id)
            questTable = db['Quest'].insert({
                'name': name,
                'status': status,
                'difficulty': difficulty,
                'exp': exp,
                'money': money,
                'ord': ord,
                'player_id': player_id,
                'note': note
            })
            new_quest = self.get_by_id(questTable.last_rowid)
            return make_response(new_quest, 200)
        except sqlite3.IntegrityError:
            logging.exception(sqlite3.IntegrityError)
            return make_response('User not existed', 400)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
    
    def update_quest(self, request):
        try:
            id = request.form.get('id')
            name = request.form.get('name')
            difficulty = request.form.get('difficulty')
            note = request.form.get('note')

            res = self.get_by_id(id)
            if res.status_code != 200:
                return res
            quest = json.loads(res.data)
            print("quest", quest)
            seed = quest['seed']
            if seed == None:
                seed = randint.get()
            exp = self.__get_exp_from_difficulty(difficulty, seed)
            money = self.__get_money_from_difficulty(difficulty, seed)

            db = self.dbHelper.get_db()
            db["Quest"].update(id, {"name": name,
                                    "difficulty": difficulty,
                                    "seed": seed,
                                    "exp": exp,
                                    "money": money,
                                    "note": note})
            
            updated_quest = self.get_by_id(id)
            return make_response(updated_quest, 200)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)

    def delete_quest(self, request):
        try:
            db = self.dbHelper.get_db()
            id = request.form.get('id')
            db["Quest"].delete(id)
            return make_response('Delete quest successfully', 200)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
       
    def get_by_id(self, id):
        try:
            db = self.dbHelper.get_db()
            quest = db["Quest"].rows_where(f"id = ?",[id], limit=1)
            quest = list(quest)[0]
            return make_response(quest, 200)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
        
    def change_status(self, request):
        try:
            db = self.dbHelper.get_db()
            id = request.form.get('id')
            new_status = request.form.get('status')
            
            res = self.get_by_id(id)
            if res.status_code != 200:
                return res
            quest = json.loads(res.data)
            old_status = quest['status']

            if old_status != 'Done' and new_status == 'Done':
                playerController = PlayerController(self.dbHelper)
                res = playerController.update_stat_quest_done(quest)
                if res.status_code != 200:
                    return res
            
            if old_status == 'Done' and new_status != 'Done':
                playerController = PlayerController(self.dbHelper)
                res = playerController.update_stat_quest_undone(quest)
                if res.status_code != 200:
                    return res
                 
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
        
    def change_ord(self, request):
        try:
            db = self.dbHelper.get_db()
            id = request.form.get('id')
            ord = request.form.get('ord')
            
            db["Quest"].update(id, {"ord": ord})
            return make_response('Order updated successfully', 200)
        except sqlite3.IntegrityError:
            logging.exception(sqlite3.IntegrityError)
            return make_response('Order not existed', 400)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
    
    def __get_exp_from_difficulty(self, difficulty, seed):
        return randint.get(seed, QuestController.difficulty_exp_map[difficulty])
    
    def __get_money_from_difficulty(self, difficulty, seed):
        return randint.get(seed + 1, QuestController.difficulty_exp_map[difficulty])*2


    