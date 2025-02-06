import json
from flask import jsonify
from sqlite_utils.utils import sqlite3
import logging
from flask import make_response

class PlayerController:
    exp_2_lv_up = 300
    
    def __init__(self, dbHelper):
        self.dbHelper = dbHelper
        
    def create_account(self, request):
        try:
            db = self.dbHelper.get_db()
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            # Ensure name, email, and password are provided
            if not name or not email or not password:
                return make_response('Name, email and password are required', 400)

            # Insert data into the Player table
            result = db['Player'].insert({
                'name': name,
                'email': email,
                'password': password
            })
            print(result)
            return make_response('Account created successfully', 201)
        
        except sqlite3.IntegrityError:
            return make_response('Email already existed', 400)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
        
    def login(self, request):
        try:
            db = self.dbHelper.get_db()
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                return make_response('Email and password are required', 400)

            player = db["Player"].rows_where(f"email = ?",[email], limit=1)
            player = list(player)[0]
            
            if player['password'] == password:
                return make_response('Login successfully', 202)

            raise Exception('Login failed')
            
        except Exception as e:
            logging.exception(e)
            return make_response('Incorrect Email or Password', 401)
        
    def get_player_by_email(self, email):
        try:
            db = self.dbHelper.get_db()

            player = db["Player"].rows_where(f"email = ?",[email], limit=1, 
                                            select="id, email, name, level, exp, money, progress")
            player = list(player)[0]
            
            return make_response(player, 200)
            
        except Exception as e:
            logging.exception(e)
            return make_response('Can not find player', 404)

    def get_by_id(self, id):
        try:
            db = self.dbHelper.get_db()
            player = db["Player"].rows_where(f"id = ?",[id], limit=1)
            player = list(player)[0]
            return make_response(player, 200)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
        
    def update_stat_quest_done(self, quest):
        res = self.get_by_id(quest['player_id'])
        if res.status_code != 200:
            return res
        player = json.loads(res.data)
        
        try:
            money = player['money'] + quest['money']
            exp = player['exp'] + quest['exp']
            lv = exp//PlayerController.exp_2_lv_up
            progress = (exp % PlayerController.exp_2_lv_up) * 100 / PlayerController.exp_2_lv_up
            progress = round(progress, 2)
            
            db = self.dbHelper.get_db()
            db["Player"].update(quest['player_id'], 
                                {"level": lv, "exp": exp, 
                                "money": money, "progress": progress})

            return make_response('Player stat update successfully', 200)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
    
    def update_stat_quest_undone(self, quest):
        res = self.get_by_id(quest['player_id'])
        if res.status_code != 200:
            return res
        player = json.loads(res.data)
        
        try:
            money = player['money'] - quest['money']
            exp = player['exp'] - quest['exp']
            lv = exp//PlayerController.exp_2_lv_up
            progress = (exp % PlayerController.exp_2_lv_up) * 100 / PlayerController.exp_2_lv_up
            progress = round(progress, 2)
            
            db = self.dbHelper.get_db()
            db["Player"].update(quest['player_id'], 
                                {"level": lv, "exp": exp, 
                                "money": money, "progress": progress})

            return make_response('Player stat update successfully', 200)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
        
    def get_id_by_email(self, email):
        try:
            db = self.dbHelper.get_db()
            id = db["Player"].rows_where(f"email = ?",[email], limit=1, select="id")
            id = list(id)[0]
            return make_response(id, 200)
        except Exception as e:
            logging.exception(e)
            return make_response('Can not find player', 404)