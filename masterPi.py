import json
import csv

#we get data from Matt
tag_data = None;
with open('data.txt') as json_data:
    tag_data = json.load(json_data);

master1writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
for tag in tag_data:
    regions = set();
    data = tag_data[tag];
    
    cmp_tag = lambda(x, y): return cmp(x[2], y[2]);
    s_data = sorted(data, cmp=cmp_tag);

    # tag-entry data is sorted by timestamp (naive)
    for next_event in s_data: 
        # next_event has format: (readId, e/l, ts)
        if (next_event[1] == True):
            regions.add(readId);
        else:
            regions.remove(readId);
        
        if (len(regions)) == 1):
            

    master1writer.writerow(['TagID'+ ';' + 'e/l'+ ';' + 'ReaderID' + ';' + 'time'])
    
# Send csv to database

