#! /usr/bin/env python

# TODO
# 
# LEN(1), ADDR(1), COMMAND(1), DATA(var), CRCLSB(1), CRCMSB(1)
# Neil Ryan <nryan@andrew.cmu.edu>

import serial

TAG_LENGTH = 18
MSG_FORMATTER = "%c%c%c%s"
PRESET_VALUE = 0xFFFF
POLYNOMAIL = 0x8408

def crc(data):
    val = PRESET_VALUE
    for i in xrange(len(data)):
        val ^= data[i]
        for j in xrange(8):
            if (val & 0x1):
                val = (val >> 1) ^ POLYNOMIAL
            else:
                val = val >> 1
    return val
    
# Command - int
# Data - List of bytes
def sendCommand(command, data):
    msg_data = [1,1].append(command)
    msg_data += data
    crc_val = crc(msg_data)
    msg_data += crc_val & 0xFF
    msg_data += (crc_val >> 8) & 0xFF
    data_str = ""
    for byte in msg_data:
        data_str += chr(byte)

    ser.write(data_str)
    

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
