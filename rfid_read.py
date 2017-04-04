#! /usr/bin/env python

# Reads from a reader attached at /dev/ttyUSB0 and prints the tags
# that get sensed to STDOUT
# 
#
# Neil Ryan <nryan@andrew.cmu.edu>

import serial

TAG_LENGTH = 18

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate='57600',
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while(1):
    x = ser.readline(TAG_LENGTH)
    if x:
        print(str(x.encode('hex')))
