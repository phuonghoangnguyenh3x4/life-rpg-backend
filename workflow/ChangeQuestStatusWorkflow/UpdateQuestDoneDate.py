from workflow.Task import Task
from services.quest.update_quest_service import UpdateQuestService
from services.quest.get_quest_service import GetQuestService
from utils.quest_utils import isQuestMadeDone, isQuestMadeUndone
import datetime
import json
from dateutil.parser import parse
class UpdateQuestDoneDate(Task):
    def execute(self, context):
        db_helper = context['db_helper']
        update_quest_service = UpdateQuestService(db_helper)
        get_quest_service = GetQuestService(db_helper)
        id: int = context['quest_id']
        old_status = context['old_status']
        new_status = context['new_status']

        if isQuestMadeDone(old_status, new_status):
            now = datetime.datetime.today()
            context['done_date'] = now
            res = update_quest_service.change_done_date(id, now)
            if res.status_code != 200:
                raise Exception(res)
            
        if isQuestMadeUndone(old_status, new_status):
            res = get_quest_service.get_done_date(id)
            if res.status_code != 200:
                raise Exception(res)
            done_date = json.loads(res.data)['done_date']
            done_date = parse(done_date)

            context['done_date'] = done_date
            res = update_quest_service.remove_done_date(id)
            if res.status_code != 200:
                raise Exception(res)