from dotenv import load_dotenv
from flask import request, Flask
from flask_cors import CORS
import os
from helpers.db_helper import DBHelper
from controllers.player_controller import PlayerController

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

dbHelper = DBHelper(DB_URL)

app = Flask(__name__)
CORS(app)

@app.route('/create-account', methods=["POST"])
def create_account():
    playerController = PlayerController(dbHelper)
    return playerController.create_account(request)

@app.route('/login', methods=["POST"])
def login():
    playerController = PlayerController(dbHelper)
    return playerController.login(request)

@app.route('/get-users')
def get_users():
    db = dbHelper.get_db()
    for row in db["Player"].rows:
        print(row)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
