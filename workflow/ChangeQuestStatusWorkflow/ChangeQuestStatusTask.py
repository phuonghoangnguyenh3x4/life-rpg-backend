from workflow.Task import Task
from services.quest.update_quest_service import UpdateQuestService

class ChangeQuestStatusTask(Task):
    def execute(self, context):
        db_helper = context['db_helper']
        update_quest_service = UpdateQuestService(db_helper)
        id: int = context['quest_id']
        new_status = context['new_status']
        
        res = update_quest_service.change_status(id, new_status)
        if res.status_code != 200:
            raise Exception(res)