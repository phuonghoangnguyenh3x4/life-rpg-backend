from utils.factory import createDBHelper
from services.heatmap.get_heatmap_service import GetHeatmapService
import datetime

dbHelper = createDBHelper()
GetHeatmapService(dbHelper).get_count(datetime.date.today())