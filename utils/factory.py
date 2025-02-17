from utils.db_utils import DBHelper
from services.player.get_player_service import GetPlayerService
from services.quest.get_quest_service import GetQuestService
from controllers.player_controller import PlayerController
from controllers.quest_controller import QuestController

def createGetPlayerService():
    dbHelper = DBHelper()
    return GetPlayerService(dbHelper)

def createGetQuestService():
    dbHelper = DBHelper()
    return GetQuestService(dbHelper)

def createPlayerController():
    dbHelper = DBHelper()
    return PlayerController(dbHelper)

def createQuestController():
    dbHelper = DBHelper()
    return QuestController(dbHelper)

def createDBHelper():
    return DBHelper()