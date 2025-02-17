from services.quest.get_quest_service import GetQuestService
from services.quest.create_quest_service import CreateQuestService
from services.quest.update_quest_service import UpdateQuestService
from services.quest.delete_quest_service import DeleteQuestService
from wrappers.general_exception_handler import general_exception_handler
from wrappers.integrity_handler import integrity_error_handler
class QuestController:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._get_quest_service = GetQuestService(dbHelper)
        self._create_quest_service = CreateQuestService(dbHelper)
        self._update_quest_service = UpdateQuestService(dbHelper)
        self.delete_quest_service = DeleteQuestService(dbHelper)
        
    @general_exception_handler('Can not find quests')
    def get_quest_by_player(self, request, player_id):
        return self._get_quest_service.get_quest_by_player(request, player_id)
        
    @general_exception_handler('Can not find quest')
    def get_player_id(self, request):
        return self._get_quest_service.get_player_id(request)
    
    @general_exception_handler()
    @integrity_error_handler('User not existed')
    def create_quest(self, request, player_id):
        return self._create_quest_service.create_quest(request, player_id)
    
    @general_exception_handler()
    def update_quest(self, request):
        return self._update_quest_service.update_quest(request)

    @general_exception_handler('An error occurred')
    def delete_quest(self, request):
        return self.delete_quest_service.delete_quest(request)
    
    @general_exception_handler()
    @integrity_error_handler('Status not existed')
    def change_status(self, request):
        return self._update_quest_service.change_status(request)
    
    @general_exception_handler()
    @integrity_error_handler('Order not existed')
    def change_ord(self, request):
        return self._update_quest_service.change_ord(request)