#! /usr/bin/env python

# TODO Check CRCs coming back
# TODO assume that each packet is 17 bytes
# TODO just read data off the sensor
# TODO maybe increase scan time? Will it overflow the buffer
#
# LEN(1), ADDR(1), COMMAND(1), DATA(var), CRCLSB(1), CRCMSB(1)
# Neil Ryan <nryan@andrew.cmu.edu>

import serial

LINE_LENGTH = 18

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


# Sends a command to a serial connection
# ser: Serial connection (serial.Serial)
# command: Integer command code
# data: List of data bytes to send with command
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

# Recieves data from a serial connection
# ser: Serial connection (serial.Serial)
def recieveData(ser):
    data = []
    # Get first line (so we know length)
    while 1:
        x = ser.readline(LINE_LENGTH)
        if x:
            first_line = toBytes(x)
            print(first_line)
            data_len = int(first_line[0], 16)
            data_len -= len(first_line) + 1 # len doesn't include len byte
            print("len = {}".format(data_len))
            data.append(first_line)
            break
    # Get the rest of the data
    while data_len > 0:
        x = ser.readline(LINE_LENGTH)
        if x:
            line = toBytes(x)
            data_len -= len(line)
            data.append(line)
    data = flatten(data)
    crc_data = data[1:-2]
    for i in xrange(len(crc_data)):
        crc_data[i] = int(crc_data[i], 16)
    data_crc = crc(crc_data)
    print(hex(data_crc))

    return data


# Prints response data with some formatting
# data: Array of data bytes (as strings) to print
def printData(data):
    assert(len(data) >= 6) # Len, Adr, reCmd, Status, CRCLSB, CRCMSB
    data_len = len(data) - 4
    print("Length: {}".format(int(data[0], 16)))
    print("Address: 0x{}".format(data[1]))
    print("Response Command {}".format(data[2]))
    print("Status: 0x{}".format(data[3]))

    s = ""
    num_bytes = 0
    for i in xrange(4, data_len - 2):
        s += "0x{} ".format(data[i])
        num_bytes += 1
        if num_bytes % 8 == 0:
            s += "\n\t"

    print("Data: {}".format(s))
    print("CRC: 0x{}{}".format(data[data_len-1], data[data_len-2]))


# Sets the power level of the reader
def setPower(ser, power_level):
    assert(power_level >= 0 and power_level <= 30)
    sendCommand(ser, 0x2f, [power_level])
    data = recieveData(ser)
    printData(data)

# Get the work mode parameter of the reader
def getReaderInfo(ser):
    sendCommand(ser, 0x21, [])
    data = recieveData(ser)
    printData(data)


# Get the work mode parameter of the reader
def getWorkMode(ser):
    sendCommand(ser, 0x36, [])
    data = recieveData(ser)
    printData(data)


# Set the address that the reader will listen at
def setAddress(ser, address):
    sendCommand(ser, 0x24, [address])
    data = recieveData(ser)
    printData(data)

# Set the InventoryScanTime of the reader
def setScanTime(ser, scan_time):
    sendCommand(ser, 0x25, [scan_time])
    data = recieveData(ser)
    printData(data)

# Set the LED light flash/buzzer tweet
# activeT: LED flash and buzzer tweet time
# silentT: LED and buzzer silent time
# times: LED flash and buzzer tweet times
def acoustoOpticControl(ser, activeT, silentT, times):
    sendCommand(ser, 0x33, [activeT, silentT, times])
    data = recieveData(ser)
    printData(data)


# Set the reader information - see docs for definitions
def setWorkMode(ser, read_mode, mode_state, mem_inven,
        first_adr, word_num, tag_time):
    sendCommand(ser, 0x35,
            [read_mode, mode_state, mem_inven,
                first_adr, word_num, tag_time])
    data = recieveData(ser)
    printData(data)


# Get the reader information
def getWorkCommand(ser):
    sendCommand(ser, 0x36, [])
    data = recieveData(ser)
    printData(data)


# Inventory one tag (6B) in effective field
# If >1 tag in range, reader may get nothing
def inventorySignal(ser):
    sendCommand(ser, 0x50, [])
    data = recieveData(ser)
    printData(data)



def setBaudRate(ser, rate):
    sendCommand(ser, 0x28, [rate])
    data = recieveData(ser)
    printData(data)


# Inventory tags in effective field and get ID values
# condition: Condition of detecting tags
# addr: Tag's start address to compare
# mask: data used to compare
# wordData: array used to compare (8 bytes long)
def inventoryMultiple(ser, condition, addr, mask, wordData):
    wdata = flatten([condition, addr, mask, wordData])
    sendCommand(ser, 0x51, wdata)
    data = recieveData(ser)
    printData(data)


def read(ser, data):
    sendCommand(ser, 0x2, data)
    data = recieveData(ser)
    printData(data)


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate='115200',
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

getReaderInfo(ser)
#sendCommand(ser, 0x35, [2, 0x2, 0x4, 0x0, 0x12, 0x0])
#sendCommand(ser, 0x36, []) #Gets work mode
#sendCommand(ser, 0x21, [])
