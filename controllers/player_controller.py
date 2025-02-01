from flask import jsonify
from sqlite_utils.utils import sqlite3
import logging
from flask import make_response

class PlayerController:
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
                return jsonify({'error': 'Name, email and password are required'}), 400

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

            player = db["Player"].rows_where(f"email = ?",[email], limit=1)
            player = list(player)[0]
            
            if player['password'] == password:
                return make_response('Login successfully', 202)

            raise Exception('Login failed')
            
        except Exception as e:
            logging.exception(e)
            return make_response('Incorrect Email or Password', 401)
        
    def (self, email):
        try:
            db = self.dbHelper.get_db()

            player = db["Player"].rows_where(f"email = ?",[email], limit=1, 
                                             select="id, email, name, level, exp, money")
            player = list(player)[0]
            
            return make_response(player, 200)
            
        except Exception as e:
            logging.exception(e)
            return make_response('Can not find player', 404)get_player_by_email