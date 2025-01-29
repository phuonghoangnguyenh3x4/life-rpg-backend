class Migrator:
    def __init__(self, db):
        self.db = db

    def migrate(self):
        self.__createUserTable()
        
    def __createUserTable(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS Player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            ''')