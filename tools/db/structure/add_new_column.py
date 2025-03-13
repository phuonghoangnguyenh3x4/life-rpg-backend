from dotenv import load_dotenv
import sqlite_utils
import os
import datetime

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Initialize the SQLite connection with thread safety
db = sqlite_utils.Database(DB_URL)

# db["Quest"].add_column("done_date", datetime.date)
db["Heatmap"].add_column("player_id")
db["Heatmap"].insert()
pk=("breed", "id")