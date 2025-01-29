from migrator import Migrator
from dotenv import load_dotenv
import sqlite_utils
import os

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Initialize the SQLite connection with thread safety
db = sqlite_utils.Database(DB_URL)

# Perform migrations
migrator = Migrator(db)
migrator.migrate()
