from flask import make_response

class DeleteQuestService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper

    def delete_quest(self, request):
        db = self._dbHelper.get_db()
        id = request.form.get('id')
        db["Quest"].delete(id)
        return make_response('Delete quest successfully', 200)