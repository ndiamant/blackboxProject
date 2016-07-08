import os
import payloadReader
import time


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
                        textList.append(filterByText(payloadReader.readFiles(indexList), targetText))
                        os.remove(os.path.join(targetDirectory, payload))

        payloadReader.writeByFileID(textList, targetDirectory)
        end = time.time()
        print 'Time elapsed: ' + str(end - start) + ' seconds' 
        return textList


def bigTextList(indexDirectory, payloadDirectory, willFilter = False, targetText = None):
        """
        Goes through all of the index files from indexDirectory, finds matching payload files from
        payloadDirectory and returns a text list. Files are assumed to be named like they are
        on the white box server.
        """

        start = time.time()
        finalList = []
        for p, d, f in os.walk(indexDirectory): # path, directories, files
                f = sorted(filter(lambda x: "index" in x and '#' not in x, f)) # make sure only using index files in time increasing order               
                time1, time2 = 0, time.time()
                for filesRead, file in enumerate(f): 
                        # print progress
                        if filesRead % 10 == 0 and not filesRead == 0:
                                time1, time2 = time2, time.time()
                                percentDone = 100.0 *  filesRead / len(f)
                                print '{:.3f}% done\nLast batch done in {:.3f} seconds at {:.3f} files per second.'.format(percentDone, time2 - time1, 10 / (time2 - time1))

                        payload = 'payload-' + file[6:]
                        indexList = payloadReader.createIndexList(file, indexDirectory)
                        if willFilter:
                                textList = payloadReader.readFiles(payload, indexList, payloadDirectory, True, targetText)
                        else: 
                                textList = payloadReader.readFiles(payload, indexList, payloadDirectory)
                        finalList += textList
                        textList = []
                        indexList = []
                break
        end = time.time()
        print 'Time elapsed: ' + str(end - start) + ' seconds' 
        return finalList