from workflow.Task import Task
from services.quest.create_quest_service import CreateQuestService
import json

class CreateQuestTask(Task):
    def execute(self, context):
        db_helper = context['db_helper']
        create_quest_service = CreateQuestService(db_helper)

        request = context['request']
        player_id = context['player_id']
        res = create_quest_service.create_quest(request, player_id)
        if res.status_code != 200:
            raise Exception(res)
        
        quest = json.loads(res.data)
        context['new_quest'] = quest