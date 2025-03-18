from workflow.Task import Task
from services.player.update_player_service import UpdatePlayerService
from enums.quest_status import QuestStatus
class UpdatePlayerStatTask(Task):     
    def execute(self, context):
        db_helper = context['db_helper']
        quest = context['quest']
        update_player_service = UpdatePlayerService(db_helper)
        if quest['status'] != QuestStatus.Done:
            return
        update_player_service.update_stat_quest_undone(quest)