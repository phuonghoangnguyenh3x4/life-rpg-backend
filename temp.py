from dotenv import load_dotenv
import sqlite_utils
import os

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Initialize the SQLite connection with thread safety
db = sqlite_utils.Database(DB_URL)

# db["Quest"].delete(10)

# res = db.execute('''
#     SELECT SUM(exp)
#     FROM Quest
#     Where player_id = 1 and status = "Done"
#     ''')



# money = 1964
# exp = 1151
# exp_2_lv_up = 300
# lv = exp//exp_2_lv_up
# progress = (exp % exp_2_lv_up) * 100 / exp_2_lv_up
# progress = round(progress, 2)

# res = db["Player"].update(1, {"level": lv, "exp": exp, "money": money})
# db["Quest"].add_column("note", str)

# db["Player"].update(1, {"progress": progress})

# print(list(res))
# '0|000000:', 
# orders = ['0|100000:', '0|100008:', '0|10000g:', '0|10000o:', '0|10000w:', '0|100014:', '0|10001c:', '0|10001k:', '0|10001s:', '0|100020:', '0|100028:', '0|10002g:', '0|10002o:', '0|10002w:', '0|100034:']

# print(sorted(orders))

# db['Quest'].transform(rename={"order": "ord"})
# res = db["Quest"].rows_where('player_id = ? and status = ?', [1, 'Done'], order_by='ord asc', select='id') 
# ids = list(res)
# ids = [id['id'] for id in ids]
# # print(ids)
# # ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17]

# for i in range(len(ids)):
#     db["Quest"].update(ids[i], {"ord": orders[i]})


# res = db["Quest"].rows_where() 
# res = list(res)

# for i in range(22,84):
#     db["Quest"].delete(i)

db["Quest"].delete(39)


