from dotenv import load_dotenv
import sqlite_utils
import os
import datetime

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

db = sqlite_utils.Database(DB_URL)

# db["QuestDone"].create({
#     "quest_id": int,
#     "done_date": str,
# }, pk="quest_id")

db["Heatmap"].create({
    "date": datetime.date,
    "count": int,
}, pk="date")

