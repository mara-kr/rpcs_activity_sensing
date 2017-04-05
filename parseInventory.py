#there could be cleaner ways to write this
#but oh well ¯\_(ツ)_/¯

def parseInventory(response):
	#length is 1 byte
	length = int(response[0] ,16) + int(response[1], 16)
	#addr is 1 byte
	addr = response[2]+ response[3]
	#reCmd is 1 byte
	reCmd = response[4] + response[5]
	#status is 1 byte
	status = response[6] + response[7]
	#5 bytes of length are adr, reCmd,status, lsb CRC, msb CRC
	dataLen = length - 10
	data = response[8:dataLen]

	#number of data elements is 1 byte
	numDataElements = int(data[0], 16) + int(data[1], 16)
	#ignore the number byte
	data = data[2:]
	#dataLen - 2 is the number of bytes in data that has actual values
	for i in range(0, dataLen - 2):
		epcLen = int(epcData[i] + epcData[i+1], 16)
		tidLen = int(epcData[i+2] + epcData[i+3], 16)
		tidData = epcData[i+4:i+4+tidLen]
		print("TID %d Data: %x \n", i, tidData)

		i += epcLen
	print(str(length) + " length, " + str(addr) + " addr, " + str(reCmd) + " reCmd, " + str(status) + " status, " + str(dataLen) + " dataLen, " + str(data) + " data\n")
parseInventory("080000000000")