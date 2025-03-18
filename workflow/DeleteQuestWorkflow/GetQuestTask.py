from workflow.Task import Task
import json
from services.quest.get_quest_service import GetQuestService

class GetQuestTask(Task):     
    def execute(self, context):
        db_helper = context['db_helper']
        get_quest_service = GetQuestService(db_helper)
        id: int = context['quest_id']
        
        res = get_quest_service._get_by_id(id)
        if res.status_code != 200:
            raise Exception(res)
        quest = json.loads(res.data)
        context['quest'] = quest