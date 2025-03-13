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

# res = db["Quest"].rows

# res = db["Quest"].rows_where('name like "%Test datetime%"')

# res = db["Heatmap"].rows

# print(list(res))

if len(sys.argv) < 2:
    print("Usage: python -m tools.db.select_all <table_name>")
    sys.exit(1)

table_name = sys.argv[1]

try:
    res = db[table_name].rows
    print(list(res))
except KeyError:
    print(f"Error: Table '{table_name}' not found in the database.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)