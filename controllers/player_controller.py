from wrappers.general_exception_handler import general_exception_handler
from wrappers.integrity_handler import integrity_error_handler
from services.player.account_service import AccountService
from services.player.get_player_service import GetPlayerService
from services.player.update_player_service import UpdatePlayerService
class PlayerController:    
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._account_service = AccountService(dbHelper)
        self._get_player_service = GetPlayerService(dbHelper)
        self._update_player_service = UpdatePlayerService(dbHelper)
        
    @general_exception_handler()
    @integrity_error_handler('Email already existed')
    def create_account(self, request):
        return self._account_service.create_account(request)
    
    @general_exception_handler('Incorrect Email or Password', 401)
    def login(self, request):
        return self._account_service.login(request)
    
    def logout(self):
        return self._account_service.logout()
    
    @general_exception_handler('Can not find player', 404)
    def get_player_by_email(self, email):
        return self._get_player_service.get_player_by_email(email)

    @general_exception_handler()
    def get_by_id(self, id):
        return self._get_player_service.get_by_id(id)
    
    @general_exception_handler('Can not find player', 404)
    def get_id_by_email(self, email):
        return self._get_player_service.get_id_by_email(email)