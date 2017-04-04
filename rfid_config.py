#! /usr/bin/env python

# TODO
# 
# LEN(1), ADDR(1), COMMAND(1), DATA(var), CRCLSB(1), CRCMSB(1)
# Neil Ryan <nryan@andrew.cmu.edu>

import serial

TAG_LENGTH = 18
POLYNOMAIL = 0x8408


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
    
# Command - int
# Data - List of bytes
def sendCommand(ser, command, data):
    msg_data = [len(data) + 4,0xFF]
    msg_data.append(command)
    msg_data += data
    crc_val = crc(msg_data)
    msg_data.append(crc_val & 0xFF)
    msg_data.append((crc_val >> 8) & 0xFF)
    data_str = ""
    for byte in msg_data:
        print(hex(byte))
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

sendCommand(ser, 0x33, [0, 0xFF, 0xFF])
print('\n')
a = 1
while (a > 0):
    x = ser.readline(TAG_LENGTH)
    if x:
        x = x.encode('hex')
        s = ""
        for i in xrange(len(x)):
            s += x[i]
            if (i % 2 == 1):
                s += ' '
        print(s)
        a -= 1
