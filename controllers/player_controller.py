from flask import jsonify
from sqlite_utils.utils import sqlite3
import logging

class PlayerController:
    def __init__(self, dbHelper):
        self.dbHelper = dbHelper
        
    def create_account(self, request):
        try:
            db = self.dbHelper.get_db()
            email = request.form.get('email')
            password = request.form.get('password')

            # Ensure name, email, and password are provided
            if not email or not password:
                return jsonify({'error': 'email, and password are required'}), 400

            # Insert data into the Player table
            result = db['Player'].insert({
                'email': email,
                'password': password
            })
            print(result)
            return jsonify({'message': 'Account created successfully'}), 201
        
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Email already existed'}), 400
        except Exception as e:
            logging.exception(e)
            return jsonify({'error': 'An error occurred'}), 500
        
    def login(self, request):
        try:
            db = self.dbHelper.get_db()
            email = request.form.get('email')
            password = request.form.get('password')

            player = db["Player"].rows_where(f"email = ?",[email], limit=1)
            player = list(player)[0]
            
            if player['password'] == password:
                return jsonify({'message': 'Login successfully'}), 202

            raise Exception('Login failed')
            
        except Exception as e:
            logging.exception(e)
            return jsonify({'error': 'Incorrect Email or Password'}), 401