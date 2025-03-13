from dotenv import load_dotenv
import sqlite_utils
import os
import datetime

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

db = sqlite_utils.Database(DB_URL)

res = db.tables
print(res)