#we get data from Matt


#open file in json and parse


#conflict resolutions

#put data into csv
import csv
with open('master1.csv', 'a') as csvfile:
    master1writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    master1writer.writerow(['TagID'+ ';' + 'e/l'+ ';' + 'ReaderID' + ';' + 'time'])
    
# Send csv to database
