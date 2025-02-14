class Migrator:
    def __init__(self, db):
        self.db = db

    def migrate(self):
        self.__createUserTable()
        self.__createQuestTable()
        
    def __createUserTable(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS Player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                level INTEGER DEFAULT 1,   
                exp INTEGER DEFAULT 0,     
                progress FLOAT DEFAULT 0.0,     
                money INTEGER DEFAULT 0    
            )
            ''')
        
    def __createQuestTable(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS Quest (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status TEXT CHECK(status IN ('Todo', 'Doing', 'Done')) NOT NULL,
                difficulty TEXT CHECK(difficulty IN ('Trivial', 'Easy', 'Normal', 'Hard', 'SuperHard')) NOT NULL,
                exp INTEGER,
                money INTEGER,
                order TEXT,
                player_id INTEGER NOT NULL,
                note TEXT,
                seed INTEGER,
                FOREIGN KEY (player_id) REFERENCES Player(id)
            )
            ''')