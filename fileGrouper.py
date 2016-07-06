import os
import payloadReader
import time
import glob
import shutil


def downloadFiles(indexDirectory, targetDirectory, targetText, userName):
        """
        Takes a directory, indexDirectory, of index files assumed to be named like they are
        on the white box server, a directory to download them into, targetText to be searched for,
        and the user's whitebox user name. Returns textList if further filtering is desired.
        """
        start = time.time()
        textList = []
        for p, d, f in os.walk(indexDirectory): # path, directories, files
                f = filter(lambda x: "index" in x, f) # make sure only using index files
                for file in f:
                        payload = 'payload-' + file[6:]
                        scpCommand = 'scp ' + userName + '@white.kent.ac.uk:/data/compile-inputs/' + payload + ' ' + targetDirectory
                        os.system(scpCommand)
                        indexList = payloadReader.createIndexList(file, indexDirectory)
                        textList.append(filterByText(readFiles(indexList), targetText))
                        os.remove(os.path.join(targetDirectory, payload))

        writeByFileID(textList, targetDirectory)
        end = time.time()
        print(end - start)
        return textList


def bigTextList(indexDirectory, payloadDirectory):
        """
        Goes through all of the index files from indexDirectory, finds matching payload files from
        payloadDirectory and returns a text list. Files are assumed to be named like they are
        on the white box server.
        """

        start = time.time()
        finalList = []
        for p, d, f in os.walk(indexDirectory): # path, directories, files
                f = filter(lambda x: "index" in x, f) # make sure only using index files
                filesRead = 0
                for file in f:
                        percentDone = 100.0 *  filesRead / len(f)
                        if filesRead % 10 == 0:
                                print '{:.3f} percent done'.format(percentDone)
                        payload = 'payload-' + file[6:]
                        indexList = payloadReader.createIndexList(file, indexDirectory)
                        textList = payloadReader.readFiles(payload, indexList, payloadDirectory)
                        finalList += textList
                        filesRead += 1
                break
        end = time.time()
        print(end - start)
        return textList              

# def groupByFileID(payloadDirectory, targetDirectory):
#         """
#         uses a directory built by getTextFiles and groups text by 
#         """
#         IDlist = []
#         name = 0
#         paths = glob.glob(payloadDirectory + os.sep + '/*/*') # make / os.sep
#         for path in paths:
#                 ID = os.path.basename(os.path.normpath(path))
#                 targetDir = targetDirectory  + os.sep + ID
#                 if ID not in IDlist:
#                         os.mkdir(targetDir)
#                         IDlist.append(ID)
#                 for p, d, f in os.walk(path):
#                         for file in f:
#                                 dst = targetDir + os.sep + 'payload' + str(name) + '.java'
#                                 src = path + os.sep + file
#                                 shutil.copyfile(src, dst)
#                                 name += 1


