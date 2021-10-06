from tinydb import TinyDB, Query
import json
import os


try:
   os.remove('db.json')
except:
   pass

db = TinyDB('db.json')

with open('example.json') as json_file:
   record=json.load(json_file)
db.insert(record)


