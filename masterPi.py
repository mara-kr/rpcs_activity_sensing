#! /usr/bin/env python

# Script to run on the master node to filter data and send to database

import os
import datetime
import requests

DATA_FILE_DIR = "/home/pi/data/"
COMPOUND_DATA_FILE = DATA_FILE_DIR + "master_compound.csv"
FILTERED_DATA_FILE = DATA_FILE_DIR + "master_filtered.csv"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_THRESHOLD = 5  # Seconds between TODO, have entering/leaing
COUNT_SEND_THRESHOLD = 10
POST_URL = "http://128.237.197.65:3000/sensors/reeive"
POST_HEADERS = {'content-type': 'text/csv'}


class DataLine:
    def __init__(self, line):
        data = line.strip().split(';')
        print(data)
        self.readerID = data[0]
        self.tagID = data[1]
        self.time = data[2]
        self.datetime = datetime.datetime.strptime(self.time, TIME_FORMAT)
        self.entering = data[3]

    def __lt__(self, other):
        if isinstance(other, DataLine):
            return self.datetime < other.datetime
        else:
            return False

    def __str__(self):
        if (self.entering == 'true'):
            status_str = "true"
        else:
            status_str = "false"
        return "{};{};{};{};{}\n".format(self.readerID, self.time,
                self.tagID, status_str, "activity_sensing")


class DataFile:
    def __init__(self, fname):
        self.fname = DATA_FILE_DIR + fname
        self.handler = open(self.fname, 'r')
        print(self.fname)
        self.last_line = DataLine(self.handler.readline())

    def newline(self):
        line = self.handler.readline()
        if (len(line) == 0):
            return line
        print(self.fname)
        self.last_line = DataLine(line)
        return line


# Sort the data from multiple files by timestamp
# Map reduce with one node - probably shouldn't be in python
def createCompoundFile():
    data_files = []
    data_fnames = os.listdir(DATA_FILE_DIR)

    for fname in data_fnames:
        if ('master' not in fname):
            data_files.append(DataFile(fname))

    out_f = open(COMPOUND_DATA_FILE, 'w')

    while (len(data_files) > 0):
        min_line = data_files[0].last_line
        min_i = 0
        for i in xrange(1, len(data_files)):
            if data_files[i].last_line < min_line:
                min_line = data_files[i].last_line
                min_i = i

        out_f.write(str(min_line))
        if len(data_files[min_i].newline()) == 0:  # File is empty
            data_files[min_i].handler.close()
            #os.remove(data_files[min_i].fname)  # Cleanup file
            data_files.pop(min_i)

    out_f.close()  # Flush writes to disk


# Do conflict detection on the sorted data stream
def filterCompoundFile():
    data_f = open(COMPOUND_DATA_FILE, 'r')
    out_f = open(FILTERED_DATA_FILE, 'w')

    # Store buffer of data that's within the time range
    history_buffer = []
    # Track whether there was a conflict with the current line
    no_conflict = True
    remove_lines = []

    # Conflict detection
    for line in data_f:
        curr_line = DataLine(line)
        no_conflict = True
        remove_lines = []
        for seen_line in history_buffer:
            # Check for tag match in buffer - if so, remove both
            if (seen_line.tagID == curr_line.tagID and
                    seen_line.readerID != curr_line.readerID and
                    seen_line.entering == curr_line.entering):
                # Append lines to remove so we don't remove while traversing
                remove_lines.append(seen_line)
                no_conflict = False
                continue
            tdiff = curr_line.datetime - seen_line.datetime
            tdiff = int(tdiff.total_seconds())
            # When data outside range, write to file
            if (tdiff > TIME_THRESHOLD):
                out_f.write(str(seen_line))
                history_buffer.remove(seen_line)
        for line in remove_lines:
            history_buffer.remove(line)
        if (no_conflict):
            history_buffer.append(curr_line)

    data_f.close()
    # Write remaining lines
    for line in history_buffer:
        out_f.write(str(line))
    out_f.close()


if __name__ == "__main__":
    createCompoundFile()
    filterCompoundFile()

    # Send the data to the server
    f = open(FILTERED_DATA_FILE, 'r')
    count = 0;
    data = ""
    for line in f:
        data += line
        count += 1
        if (count == COUNT_SEND_THRESHOLD):
            r = requests.post(POST_URL, data = data, headers=POST_HEADERS)
            count = 0
            data = ""

    # Send the rest if we haven't sent all of it
    if (len(data) > 0):
        r = requests.post(POST_URL, files={'filtered_data.csv': f})

    f.close()
    #os.remove(FILTERED_DATA_FILE)
    #os.remove(COMPOUND_DATA_FILE)
