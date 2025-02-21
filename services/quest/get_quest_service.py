from flask import make_response
import logging
from utils.pagination_utils import get_limit_offset

class GetQuestService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper

    def _get_type_quests_count(self, player_id, type):
        db = self._dbHelper.get_db()
        count = db["Quest"].count_where("player_id = ? and status = ?", [player_id, type]) 
        return count
    
    def _get_type_quests(self, player_id, type, limit, offset): 
        db = self._dbHelper.get_db()
        quests = db["Quest"].rows_where(f"player_id = ? and status = ?", [player_id, type], order_by="ord desc", limit=limit, offset=offset)
        return list(quests)
    
    def _get_prev_page_ord_by_type(self, player_id, page, per_page, type, type_count):
        offset = ((page - 1) * per_page) - 1
        if offset < 0:
            return None
        if type_count <= 0:
            return None
        if offset > type_count:
            offset = type_count - 1
        db = self._dbHelper.get_db()
        quest = db["Quest"].rows_where(f"player_id = ? and status = ?", [player_id, type], order_by="ord desc", limit=1, offset=offset)
        quest = list(quest)
        if len(quest) < 1:
            return None
        quest = quest[0]
        return quest['ord']
    
    def _get_next_page_ord_by_type(self, player_id, page, per_page, type, type_count):
        offset = ((page - 1) * per_page) + per_page
        if offset >= type_count:
            return None
        if type_count <= 0:
            return None
        db = self._dbHelper.get_db()
        quest = db["Quest"].rows_where(f"player_id = ? and status = ?", [player_id, type], order_by="ord desc", limit=1, offset=offset)
        quest = list(quest)
        if len(quest) < 1:
            return None
        quest = quest[0]
        return quest['ord']
    
    def _get_by_id(self, id):
        try:
            db = self._dbHelper.get_db()
            quest = db["Quest"].rows_where(f"id = ?",[id], limit=1)
            quest = list(quest)[0]
            return make_response(quest, 200)
        except Exception as e:
            logging.exception(e)
            return make_response('An error occurred', 500)
        
    def _get_3_type_quests(self, player_id, limit, offset):
        todos = self._get_type_quests(player_id, "Todo", limit, offset)
        doings = self._get_type_quests(player_id, "Doing", limit, offset)
        dones = self._get_type_quests(player_id, "Done", limit, offset)
        return [*todos, *doings, *dones]
    
    def _get_3_type_count(self, player_id):
        todo = self._get_type_quests_count(player_id, "Todo")
        doing = self._get_type_quests_count(player_id, "Doing")
        done = self._get_type_quests_count(player_id, "Done")
        return {
            'Todo': todo,
            'Doing': doing,
            'Done': done
        }

    def _get_prev_page_ord(self, player_id, page, per_page, type_counts):
        types = ['Todo', 'Doing', 'Done']
        res = {}
        for type in types:
            ord = self._get_prev_page_ord_by_type(player_id, page, per_page, type, type_counts[type])
            res[type] = ord
        return res
    
    def _get_next_page_ord(self, player_id, page, per_page, type_counts):
        types = ['Todo', 'Doing', 'Done']
        res = {}
        for type in types:
            ord = self._get_next_page_ord_by_type(player_id, page, per_page, type, type_counts[type])
            res[type] = ord
        return res
    
    def get_quest_by_player(self, request, player_id):
        page: int = request.args.get('page', 1, type=int)
        per_page: int = request.args.get('per_page', 5, type=int)
        limit, offset = get_limit_offset(page, per_page)

        type_counts = self._get_3_type_count(player_id)
        max_quests = max([v for k,v in type_counts.items()])
        total_quests = sum([v for k,v in type_counts.items()])
        quests = self._get_3_type_quests(player_id, limit, offset)
        prev_ord = self._get_prev_page_ord(player_id, page, per_page, type_counts)
        next_ord = self._get_next_page_ord(player_id, page, per_page, type_counts)
        
        data = {
            'total': total_quests,
            'max_quests': max_quests,
            'pages': (max_quests + per_page - 1) // per_page,
            'current_page': page,
            'per_page': per_page,
            'quests': list(quests),
            'prev_ord': prev_ord,
            'next_ord': next_ord
        }
        return make_response(data, 200)
    
    def get_player_id(self, request):
        quest_id = request.form.get('id')
        db = self._dbHelper.get_db()
        res = db["Quest"].rows_where(f"id = ?", [quest_id], select="player_id")
        quest = list(res)[0]
        return make_response(quest, 200)