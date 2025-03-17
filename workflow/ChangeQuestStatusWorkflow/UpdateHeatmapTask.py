from workflow.Task import Task
from services.heatmap.update_heatmap_service import UpdateHeatmapService
from utils.quest_utils import isQuestMadeDone, isQuestMadeUndone
import datetime

class UpdateHeatmapTask(Task):
    def execute(self, context):
        old_status = context['old_status']
        new_status = context['new_status']

        quest = context['quest']
        player_id = quest['player_id']
        db_helper = context['db_helper']
        update_heatmap_service = UpdateHeatmapService(db_helper)
        date : datetime.datetime = context['done_date']
        date = date.date()

        if isQuestMadeDone(old_status, new_status):
            update_heatmap_service.increase_count(date, player_id)

        if isQuestMadeUndone(old_status, new_status):
            update_heatmap_service.decrease_count(date, player_id)