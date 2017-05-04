#! /usr/bin/env python

# Reads data from the RFID reads at 115200 Baud, from /dev/ttyUSB0
#
# Neil Ryan <nryan@andrew.cmu.edu>
#
# TODO: Get master server path
#       Setup SSH keygen so that we don't need to SCP

import os
import serial
import datetime
import socket
import fcntl
import struct

LINE_LENGTH = 18
PORT='/dev/ttyUSB0'
BAUDRATE='115200'
T_THRESH=10 # Time threshold to register entering/leaving
SEND_TIME = datetime.time(21, 0) # 9PM
CLEAR_TIME = datetime.time(6,0) # 6AM
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATA_FILE = "datafile.csv"
MASTER = "pi@128.237.236.106:/home/pi/data/{}.csv"

class SerialReadException(Exception):
    pass

# Takes a string read from serial, translates to array of data bytes
def toBytes(data):
    data = data.encode('hex')
    data_bytes = []
    byte = ""
    for i in xrange(len(data)):
        byte += data[i]
        if (i % 2 == 1):
            data_bytes.append(byte)
            byte = ""
    return data_bytes


# Recieves data from a serial connection
# ser: Serial connection (serial.Serial)
def recieve(ser):
    while 1:
        x = ser.read(LINE_LENGTH)
        if x:
            return toBytes(x)
        else:
            raise SerialReadException


def getId(data):
    tagId = ""
    # Id doesn't include header (4 bytes) or CRC (2 bytes)
    for i in xrange(4, len(data) - 2):
        tagId += "{}".format(data[i])
    return tagId


class Tag:
    def __init__(self, tagID, first_seen, last_seen, has_entered = False):
        self.ID = tagID
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.has_entered = has_entered # 0 is not set, 1 is entering


# returns the seconds passed
def secsPassed(time1, time2):
    return abs(int((time1 - time2).total_seconds()))


def getEntry(readerID, tagID, time, entering):
    time = time.strftime(TIME_FORMAT)
    if (entering):
        status_str = "true"
    else:
        status_str = "false"
    return "{};{};{};{};{}\n".format(readerID, time,
            tagID, status_str, "activity_sensing")


# gets IP address - code from stackoverflow
def getIpAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


# checking for tags that have left the station
def cleanupTags(tags, entry_ts, time_now):
    for seen_tag in tags:
        # remove tags that have not been seen in a minute
        if secsPassed(seen_tag.last_seen, time_now) >= T_THRESH:
            if seen_tag.has_entered:
                entry = getEntry(readerID, seen_tag.ID,
                        seen_tag.last_seen, 0);
                data_f.write(entry)
                print(entry)
                tags.remove(seen_tag)


def sendToServer(readerID):
    global data_f
    data_f.close()
    remote = MASTER.format(readerID)
    os.system("scp {} {}".format(DATA_FILE,remote))
    os.remove(DATA_FILE)
    data_f = open(DATA_FILE, 'w')


ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

sentToday = 0 # Whether this slave has sent to the server today
entry_ts = [] # entries that are sent to master Pi
readerID = "".join(getIpAddress('wlan0').split('.')) #IP addr w/o .'s
trackedTags = [] # List of tags that we currently care about (in range)
data_f = open(DATA_FILE, 'w')

while(1):
    time_now = datetime.datetime.now()
    if (sentToday and time_now.time() < CLEAR_TIME):
        sentToday = 0
    if (not sentToday and time_now.time() > SEND_TIME):
        sendToServer(readerID)
        sentToday = 1
    try:
        data = recieve(ser)
        tagID = getId(data)
    except SerialReadException:
        cleanupTags(trackedTags, entry_ts, time_now)
        continue

    new_tag = Tag(tagID, time_now, time_now)

    tag_seen = False
    for seen_tag in trackedTags:
        # Tag has already been seen
        if new_tag.ID == seen_tag.ID:
            tag_seen = True

            # If we've been seeing tag for a while, regsiter entering
            if (secsPassed(seen_tag.first_seen, time_now) >= T_THRESH and
                not seen_tag.has_entered):
                seen_tag.has_entered = True
                entry = getEntry(readerID, seen_tag.ID,
                        seen_tag.first_seen, 1);
                data_f.write(entry)
                print(entry)

                break

            # Update the last seen time
            seen_tag.last_seen = time_now

    # Tag has not been seen
    if not tag_seen:
        trackedTags.append(new_tag)

    cleanupTags(trackedTags, data_f, time_now)
