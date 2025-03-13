from dotenv import load_dotenv
import sqlite_utils
import os
import datetime
from dateutil.parser import parse

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

db = sqlite_utils.Database(DB_URL)

# db["Test"].create({
#     "id": int,
#     "test_date": datetime.date,
# }, pk="id")

# db['Test'].insert({
#     'id': 1,
#     'test_date': datetime.date.today()
# })

res = db["Test"].rows


res = list(res)[0]

print(res)

print(type(parse(res['test_date'])))

print(parse(res['test_date']).date())

date: datetime.date = parse(res['test_date']).date()
print(str(date))