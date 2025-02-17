from flask import make_response
from services.player.create_player_service import CreatePlayerService

class AccountService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._create_player_service = CreatePlayerService(dbHelper)

    def create_account(self, request):
        return self._create_player_service.create_account(request)
    
    def login(self, request):
        db = self._dbHelper.get_db()
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return make_response('Email and password are required', 400)

        player = db["Player"].rows_where(f"email = ?",[email], limit=1)
        player = list(player)[0]
        
        if player['password'] == password:
            return make_response('Login successfully', 202)

        raise Exception('Login failed')
    
    def logout(self):
        res = make_response('Logout successful')
        res.set_cookie('auth_token', '', httponly=True, secure=True, samesite='none', expires=0)
        return res