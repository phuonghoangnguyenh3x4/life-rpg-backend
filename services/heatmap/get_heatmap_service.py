from flask import make_response
import datetime

class GetHeatmapService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper
    
    def get_count(self, date: datetime.date, player_id):
        db = self._dbHelper.get_db()
        res = db["Heatmap"].rows_where(f"date = ? and player_id = ?", [date, player_id], select="count")
        res = list(res)
        count = 0
        if len(res) != 0:
            count = list(res)[0]['count']
        
        return make_response(str(count), 200)