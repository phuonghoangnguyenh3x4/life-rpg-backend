from workflow.Task import Task
from services.player.update_player_service import UpdatePlayerService
from enums.quest_status import QuestStatus
class UpdatePlayerStatTask(Task):     
    def execute(self, context):
        new_quest = context['new_quest']
        db_helper = context['db_helper']

        if new_quest['status'] != QuestStatus.Done:
            return
        
        update_player_service = UpdatePlayerService(db_helper)

        res = update_player_service.update_stat_quest_done(new_quest)
        if res.status_code != 200:
            raise Exception(res)