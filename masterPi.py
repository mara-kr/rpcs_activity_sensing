
#imports
import json
import requests
import csv

entry_ts = dict()

#import json file and parse
with open('data.text') as json_data:
    entry_ts = json.load(json_data)

#conflict resolutions

#put data into csv
with open('master.csv', 'a') as csvfile:
    masterwriter = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    masterwriter.writerow(['TagID'+ ';' + 'e/l'+ ';' + 'ReaderID' + ';' + 'time'])
    
# Send csv to database - TEST THIS CODE
url =  "http://128.237.182.83:8080"
files = {'file': open('master.csv')}
response = requests.post(url, files=files)
