from workflow.Task import Task
from services.player.update_player_service import UpdatePlayerService
from utils.quest_utils import isQuestMadeDone, isQuestMadeUndone

class UpdatePlayerStatTask(Task):     
    def execute(self, context):
        db_helper = context['db_helper']
        old_status = context['old_status']
        new_status = context['new_status']
        quest = context['quest']
        update_player_service = UpdatePlayerService(db_helper)

        if isQuestMadeDone(old_status, new_status):
            res = update_player_service.update_stat_quest_done(quest)
            if res.status_code != 200:
                raise Exception(res)
        
        if isQuestMadeUndone(old_status, new_status):
            res = update_player_service.update_stat_quest_undone(quest)
            if res.status_code != 200:
                raise Exception(res)