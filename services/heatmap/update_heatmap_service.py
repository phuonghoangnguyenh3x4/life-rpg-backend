from flask import make_response
import json
from services.heatmap.get_heatmap_service import GetHeatmapService
import datetime
from sqlite_utils.db import Database

class UpdateHeatmapService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
        self._get_heatmap_service = GetHeatmapService(dbHelper)

    def increase_count(self, date: datetime.date, player_id):
        db: Database = self._dbHelper.get_db()
        res = self._get_heatmap_service.get_count(str(date), player_id)
        if res.status_code != 200:
            return res
        data_string = res.data.decode('utf-8').replace("'", '"') # decode the byte string, and replace single quotes.
        count = json.loads(data_string)
        count += 1
        db["Heatmap"].insert({"date": date,  "count": count, "player_id": player_id}, replace=True)
        return make_response("Increase count successfully", 200)