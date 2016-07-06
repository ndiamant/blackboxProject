import os 
import itertools

def createIndexList(indexFile, directory = os.getcwd()):
        """
        Takes an index file (string of its name) and what directory it's in, and converts 
        into a list of tuples with (source file id, master event id, file start position, file length, 
        compilation success [1 or 0]).
        """
        os.chdir(directory)
        indexList = []
        with open(indexFile, "rb") as f:
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
        return (read8bytes(byteList[0:8]),read8bytes(byteList[8:16]),
                        read8bytes(byteList[16:24]),read4bytes(byteList[24:28]),
                        read4bytes(byteList[28:32]))

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

def readFiles(payloadFileName, indexList, directory = os.getcwd()):
        """
        takes a list of tuples of (source file id, master event id, file start position, 
        file length, compilation success [1 or 0]) and returns the text of 
        files from the payload file in a list
        """
        os.chdir(directory)
        textList = []
        payloadFile = open(payloadFileName)
        for index in indexList:
                payloadFile.seek(index[2])
                textList.append((payloadFile.read(index[3]), index))
        payloadFile.close()
        return textList


def writeFiles(textList, directory = os.getcwd(), nameNum = 0):
        """
        writes .java files from a text list in the specified directory. nameNum
        is an iterator so that you can tell the order of the files.
        """
        os.chdir(directory)

        for text in filterForAscii(textList):
                file = open(str(nameNum) + "-" +  writeName(text[1]) + ".java", "w")
                file.write(text[0])
                file.close()
                nameNum += 1

        return nameNum

def writeName(index):
        """
        takes an index tuple (a, b, c, d, e) and returns "a_b_c_d_e".
        """
        return reduce(lambda int1, int2: str(int1) + '_' + str(int2), index)


def filterByCompilability(indexList):
        """
        returns an index list with only indices of compilable files
        """
        return filter(lambda index: index[4] == 1, indexList)


def filterForAscii(textList):
        """
        returns a textList with no text containing non ascii characters.
        Useful becuase plyj does not compile questionmarks
        """
        return filter(lambda text: all(ord(char) < 128 and ord(char) != 13 for char in text[0]), textList)


def writeByFileID(textList, directory):
        """
        write .java files from textList into directory grouped in directories
        by file ID.
        """
        textList = sorted(textList, key = lambda entry: entry[1][0])
        nameNum = 0
        # key is the file ID, group is an iterable of the all the entries corresponding to the key
        for key, group in itertools.groupby(textList, lambda entry: entry[1][0]):
                currentDir = os.path.join(directory, str(key))
                os.makedirs(currentDir)
                nameNum = writeFiles(list(group), currentDir, nameNum)


def filterByText(textList, filterText):
        """
        filters for files containing filterText
        """
        return filter(lambda text: filterText in text[0], textList)



