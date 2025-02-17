from flask import make_response

class GetPlayerService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper

    def get_player_by_email(self, email):
        db = self._dbHelper.get_db()
        player = db["Player"].rows_where(f"email = ?",[email], limit=1, 
                                        select="id, email, name, level, exp, money, progress")
        player = list(player)[0]
        return make_response(player, 200)
    
    def get_by_id(self, id):
        db = self._dbHelper.get_db()
        player = db["Player"].rows_where(f"id = ?",[id], limit=1)
        player = list(player)[0]
        return make_response(player, 200)
    
    def get_id_by_email(self, email):
        db = self._dbHelper.get_db()
        id = db["Player"].rows_where(f"email = ?",[email], limit=1, select="id")
        id = list(id)[0]
        return make_response(id, 200)