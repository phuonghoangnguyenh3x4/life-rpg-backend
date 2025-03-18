from workflow.Task import Task
from services.heatmap.update_heatmap_service import UpdateHeatmapService
from enums.quest_status import QuestStatus
from dateutil.parser import parse

class UpdateHeatmapTask(Task):
    def execute(self, context):
        quest = context['quest']
        if quest['status'] != QuestStatus.Done:
            return
        
        db_helper = context['db_helper']
        player_id = quest['player_id']
        update_heatmap_service = UpdateHeatmapService(db_helper)
        date : str = quest['done_date']
        date = parse(date).date()
        
        update_heatmap_service.decrease_count(date, player_id)