from workflow.Task import Task
from services.quest.delete_quest_service import DeleteQuestService

class DeleteQuestTask(Task):
    def execute(self, context):
        db_helper = context['db_helper']
        delete_quest_service = DeleteQuestService(db_helper)

        quest_id = context['quest_id']
        res = delete_quest_service.delete_quest(quest_id)
        if res.status_code != 200:
            raise Exception(res)