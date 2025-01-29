import sqlite_utils

class DBHelper:
    def __init__(self, url):
        self.url = url
    
    def get_db(self):
        return sqlite_utils.Database(self.url)