#! /usr/bin/env python

# TODO
# 
# LEN(1), ADDR(1), COMMAND(1), DATA(var), CRCLSB(1), CRCMSB(1)
# Neil Ryan <nryan@andrew.cmu.edu>

# Functions to send each type of command, waits for response in function
# Include parsing of status/len/etc
# Get Work command 0x36
# Set work command 0x35
# Acoustio-optic 0x33
# Set scan time 0x25
# Set power (with response)
# Set address 0x24
# Get reader info 0x21
# Inventory single 6b 0x50
# inventory multiple 0x51

import serial

TAG_LENGTH = 18


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
    msg_data = [len(data) + 4,0x0]
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

# Sets the power level of the reader
def setPower(ser, power_level):
    sendCommand(ser, 0x2f, [power_level])



#sendCommand(ser, 0x35, [2, 0x2, 0x4, 0x0, 0x12, 0x0])
sendCommand(ser, 0x36, []) #Gets work mode
#sendCommand(ser, 0x21, [])

print('')
a = 2
while (a > 0):
    x = ser.readline(32)
    if x:
        x = x.encode('hex')
        s = ""
        for i in xrange(len(x)):
            s += x[i]
            if (i % 2 == 1):
                s += ' '
        print(s)
        a -= 1
