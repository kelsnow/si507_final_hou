# building up data base 

import sqlite3
import json 


DBNAME = 'media.db'
MEDIA_JSON = 'media.json'

f_json = open(MEDIA_JSON,'r')
f_data = f_json.read()
json_data = json.loads(f_data)



