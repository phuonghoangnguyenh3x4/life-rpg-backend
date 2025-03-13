from dotenv import load_dotenv
import sqlite_utils
import os
import sys

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")
db = sqlite_utils.Database(DB_URL)

# res = db["Quest"].columns_dict
# print(res)

if len(sys.argv) < 2:
    print("Usage: python -m tools.db.list_all_columns <table_name>")
    sys.exit(1)

table_name = sys.argv[1]

try:
    res = db[table_name].columns_dict
    print(res)
except KeyError:
    print(f"Error: Table '{table_name}' not found in the database.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)