import os 

def createIndexList(fileName):
	"""
	Takes an index file and converts into a list of tuples with 
	(start position, length) [bytes].
	"""
	indexList = []
	with open(fileName, "rb") as f:
	    byte = f.read(1)
	    while byte:
	    	byteList = []
	    	for i in range(32):
	       		byteList.append(ord(byte))
	        	byte = f.read(1)
	        indexList.append(indexToTuple(byteList))
	f.close()
	return indexList


def indexToTuple(byteList):
	"""
	takes a list of 32 bytes and converts to a tuple of 
	(source file id, master event id, file start position, file length, compilation success [1 or 0]).
	"""
	
	return (read8bytes(byteList[0:8]),read8bytes(byteList[8:16]),read8bytes(byteList[16:24]),read4bytes(byteList[24:28]),read4bytes(byteList[28:32]))


def read8bytes(byteList):
	"""
	Takes a list of 8 bytes and converts to 64 bit decimal number.
	Used by indexToTuple
	"""
	return (byteList[0] * 2**56 + byteList[1] * 2**48 + byteList[2] * 2**40 + 
			byteList[3] * 2**32 + byteList[4] * 2**24 + byteList[5] * 2**16 + 
			byteList[6] * 2**8 + byteList[7])

def read4bytes(byteList):
	"""
	Takes a list of 4 bytes and converts to 64 bit decimal number.
	Used by indexToTuple
	"""
	return (byteList[0] * 2**24 + byteList[1] * 2**16 + 
		   byteList[2] * 2**8 + byteList[3])

def readFiles(payloadFileName, indexList):
	"""
	takes a list of tupes of (startPos, length) and returns the text of 
	files from the payload file in a list
	"""
	textList = []
	payloadFile = open(payloadFileName)
	for index in indexList:
		payloadFile.seek(index[2])
		textList.append(payloadFile.read(index[3]))
	payloadFile.close()
	return textList


def writeFiles(textList, directory = os.getcwd()):
	"""
	writes .java files from a text list in the specified directory
	"""
	os.chdir(directory)
	nameNum = 0
	for text in textList:
		file = open("payLoadFile" + str(nameNum) + ".java", "w")
		file.write(text)
		file.close()
		nameNum += 1


def filterByCompilability(indexList):
	"""
	returns an index list with only compilable files
	"""
	return filter(lambda index: index[4] == 1, indexList)


def filterForAscii(textList):
	"""
	returns a textList with no text containing non ascii characters.
	Useful becuase plyj does not compile questionmarks
	"""
	return filter(lambda text: all(ord(char) < 128 for char in text), textList)


fname = "index-2016-01-08"
indList = filterByCompilability(createIndexList(fname))
first1000 = filterForAscii(readFiles("payload-2016-01-08",indList[0:1000]))
writeFiles(first1000, os.getcwd() + "/javafiles")


