from dotenv import load_dotenv
import sqlite_utils
import os
import datetime
from dateutil.parser import parse
import sys

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

db = sqlite_utils.Database(DB_URL)

res = db["Heatmap"].rows_where(f"player_id = ?", [1], select="date, count")
res = list(res)
print(res)