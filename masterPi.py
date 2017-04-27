#! /usr/bin/env python

# Script to run on the master node to filter data and send to database

import os
import datetime
import requests

DATA_FILE_DIR = "/home/pi/data"
COMPOUND_DATA_FILE = "/home/pi/data/master_compound.csv"
FILTERED_DATA_FILE = "/home/pi/data/master_filtered.csv"
TIME_FORMAT = "%m/%d/%Y %H:%M:%S"
TIME_THRESHOLD = 5 # Seconds between TODO, have entering/leaing
POST_URL = "http://128.237.197.65:3000/sensors/reeive"

class DataLine:
    def __init__(self, line):
        data = line.strip().split(',')
        assert(len(data) == 4)
        self.readerID = data[0]
        self.tagID = data[1]
        self.time = data[2]
        self.datetime = datetime.strptime(self.time, TIME_FORMAT)
        self.entering = data[3]

    def __eq__(self, other):
        if isinstance(self, other):
            return self.datetime == other.datetime
        else:
            return False

    def __lt__(self, other):
        if isinstance(self, other):
            return self.datetime < other.datetime
        else:
            return False

    def __gt__(self, other):
        if isinstance(self, other):
            return self.datetime > other.datetime
        else:
            return False

    def __str__(self):
        return "{},{},{},{}\n".format(self.readerID, self.tagID,
                self.time, self.entering)

class DataFile:
    def __init__(self, fname):
        self.fname = fname
        self.handler = open(fname, 'r')
        self.last_line = self.handler.readline()

    def newline(self):
        line = self.handler.readline()
        self.last_line = DatLine(line)
        return self.last_line


data_fnames = os.listdir(DATA_FILE_DIR)
data_files = []

for fname in data_fnames:
    data_files.append(DataFile(fname))

# Map reduce with one node - probably shouldn't be in python
out_f = open(COMPOUND_DATA_FILE, 'w')
while (len(data_files) > 0):
    min_line = data_files[0].last_line
    min_i = 0
    for i in xrange(1, len(data_files)):
        if data_files[i].last_line < min_line:
            min_line = data_files[i].last_line
            min_i = i
    out_f.write(str(min_lin))
    if len(data_files[min_i].newline()) == 0: # File is empty
        data_files[min_i].handler.close()
        os.remove(data_files[min_i].fname) # Cleanup file
        data_files.pop(min_i)

out_f.close() # Flush writes to disk
data_f = open(COMPOUND_DATA_FILE, 'r')
out_f = open(FILTERED_DATA_FILE, 'w')
# Store buffer of data that's within the time range
history_buffer = []

# Conflict detection
for line in data_f:
    curr_line = DataLine(line)
    for seen_line in history_bufer:
        # Check for tag match in buffer - if so, remove both
        if (seen_line.tagID == curr_line.tag and
                seen_line.readerID != curr_line.readerID):
            history_buffer.remove(seen_line)
            continue
        tdiff = curr_line.datetime - seen_line.datetime
        tdiff = int(diff.total_seconds())
        # When data outside range, write to file
        if (tdiff > TIME_THRESHOLD):
            out_f.write(str(seen_line))
            history_buffer.remove(seen_line)
    history_buffer.append(curr_line)

data_f.close()
out_f.close()

# Send the data to the server
f = open(FILTERED_DATA_FILE, 'rb')
r = requsts.post(POST_URL, files={'filtered_data.csv' : f})
f.close()
