from services.quest.get_quest_service import GetQuestService
from services.quest.create_quest_service import CreateQuestService
from services.quest.update_quest_service import UpdateQuestService
from services.quest.delete_quest_service import DeleteQuestService
from wrappers.general_exception_handler import general_exception_handler
from wrappers.integrity_handler import integrity_error_handler
from workflow.ChangeQuestStatusWorkflow.ChangeQuestStatusWorkflow import ChangeQuestStatusWorkflow
from workflow.AddQuestWorkflow.AddQuestWorkflow import AddQuestWorkflow
from flask import make_response
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
        context = {}
        context['request'] = request
        context['player_id'] = player_id
        context['db_helper'] = self._dbHelper
        
        AddQuestWorkflow.execute(context)

        new_quest = context['new_quest']
        return make_response(new_quest, 200)
    
    @general_exception_handler()
    def update_quest(self, request):
        return self._update_quest_service.update_quest(request)

    @general_exception_handler('An error occurred')
    def delete_quest(self, request):
        return self.delete_quest_service.delete_quest(request)

    @general_exception_handler('Change status error')
    @integrity_error_handler('Status not existed')
    def change_status(self, request):
        id: int = request.form.get('id')
        new_status = request.form.get('status')
        context = {}
        context['quest_id'] = id
        context['new_status'] = new_status
        context['db_helper'] = self._dbHelper
        
        ChangeQuestStatusWorkflow.execute(context)
        return make_response('Status updated successfully', 200)
    
    @general_exception_handler()
    @integrity_error_handler('Order not existed')
    def change_ord(self, request):
        return self._update_quest_service.change_ord(request)