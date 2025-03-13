from workflow.Task import Task
from services.quest.update_quest_service import UpdateQuestService
from utils.quest_utils import isQuestMadeDone
import datetime

class UpdateQuestDoneDate(Task):
    def execute(self, context):
        db_helper = context['db_helper']
        update_quest_service = UpdateQuestService(db_helper)
        id: int = context['quest_id']
        old_status = context['old_status']
        new_status = context['new_status']

        if isQuestMadeDone(old_status, new_status):
            now = datetime.datetime.today()
            context['done_date'] = now
            res = update_quest_service.change_done_date(id, now)
            if res.status_code != 200:
                raise Exception(res)