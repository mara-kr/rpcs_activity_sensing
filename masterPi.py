
#open file in json and parse
import json

entry_ts = dict()

with open('data.text') as json_data:
    entry_ts = json.load(json_data)

#conflict resolutions

#put data into csv
import csv
with open('master1.csv', 'a') as csvfile:
    master1writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    master1writer.writerow(['TagID'+ ';' + 'e/l'+ ';' + 'ReaderID' + ';' + 'time'])
    
# Send csv to database
