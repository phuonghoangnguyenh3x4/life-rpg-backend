from services.heatmap.get_heatmap_service import GetHeatmapService
from wrappers.general_exception_handler import general_exception_handler
class HeatmapController:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._get_heatmap_service = GetHeatmapService(dbHelper)
        
    @general_exception_handler('Can not find heatmap data')
    def get_heatmap_by_player(self, player_id):
        return self._get_heatmap_service.get_by_player_id(player_id)