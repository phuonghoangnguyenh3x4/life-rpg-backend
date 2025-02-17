import sqlite_utils
from config.app_config import AppConfig

class DBHelper:
    def __init__(self, url=AppConfig.DB_URL):
        self.url = url
    
    def get_db(self):
        return sqlite_utils.Database(self.url)