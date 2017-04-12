#! /usr/bin/env python

# Reads data from the RFID reads at 115200 Baud, from /dev/ttyUSB0
#
# Neil Ryan <nryan@andrew.cmu.edu>

import serial
import sys
import argparse
import datetime

LINE_LENGTH = 18
PORT='/dev/ttyUSB0'
BAUDRATE='115200'

# Perform a CRC on data (an array of integers)
def crc(data):
    val = 0xFFFF # PRESET_VALUE
    for i in xrange(len(data)):
        val ^= data[i]
        for j in xrange(8):
            if (val & 0x1):
                val = (val >> 1) ^ 0x8408 # POLYNOMIAL value
            else:
                val = val >> 1
    return val


# Flattens a 2D array into a 1D array
def flatten(array):
    return [val for sublist in array for val in sublist]


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
    # Get first line (so we know length)
    while 1:
        x = ser.read(LINE_LENGTH)
        if x:
            return toBytes(x)


# Prints response data with some formatting
# data: Array of data bytes (as strings) to print
def printData(data, verbose):
    assert(len(data) >= 6) # Len, Adr, reCmd, Status, CRCLSB, CRCMSB
    crc_data = []
    for val in data:
        crc_data.append(int(val, 16))
    # Remove CRC values
    crc_data.pop(-1)
    crc_data.pop(-1)
    crc_val = crc(crc_data)
    data_len = len(data) - 4
    if (verbose):
        print("Length: {}".format(int(data[0], 16)))
        print("Address: 0x{}".format(data[1]))
        print("Response Command {}".format(data[2]))
        print("Status: 0x{}".format(data[3]))

    s = ""
    num_bytes = 0
    for i in xrange(4, data_len - 2):
        s += "{}".format(data[i])
        num_bytes += 1

    if (verbose):
        print("Data: {}".format(s))
        print("CRC: 0x{}{}; calc = {}".format(data[-1], data[-2],
            hex(crc_val)))
    else:
        print(s)


def getId(data):
    tagId = ""
    # Id doesn't include header (4 bytes) or CRC (2 bytes)
    for i in xrange(4, len(data) - 2):
        tagId += "{}".format(data[i])
    return tagId


ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


parser = argparse.ArgumentParser(description="Print rfid streaming reads")
parser.add_argument('-v' , '--verbose', dest='verbose',
        default=False, action='store_true',
        help="Print data packet headers and CRC check")
args = parser.parse_args()

seen = []

while(1):
    tagId = getId(recieve(ser))
    if (args.verbose):
        print("")
    if (tagId not in seen):
        seen.append(tagId)
        print("{} {}".format(tagId, datetime.datetime.now()))
