from workflow.Task import Task
from services.heatmap.update_heatmap_service import UpdateHeatmapService
from enums.quest_status import QuestStatus
from dateutil.parser import parse

class UpdateHeatmapTask(Task):
    def execute(self, context):
        new_quest = context['new_quest']
        player_id = new_quest['player_id']
        db_helper = context['db_helper']
        update_heatmap_service = UpdateHeatmapService(db_helper)
        date : str = new_quest['done_date']
        date = parse(date).date()
        
        if new_quest['status'] == QuestStatus.Done:
            update_heatmap_service.increase_count(date, player_id)