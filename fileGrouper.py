import os
import payloadReader
import time
import glob
import shutil

def getTextFiles(indexDirectory, targetDirectory, targetText, userName):
	"""
	Assumes index files are in the format found on the white box server. 
	"""
	start = time.time()

	for p, d, f in os.walk(indexDirectory): # path, directories, files
		f = filter(lambda x: "index" in x, f) # make sure only using index files
		for file in f:
			newDir = targetDirectory + os.sep + file[6:]
			payload = 'payload-' + file[6:]
			os.mkdir(newDir)
			scpCommand = 'scp ' + userName + '@white.kent.ac.uk:/data/compile-inputs/' + payload + ' ' + newDir
			os.system(scpCommand)
			indexList = payloadReader.createIndexList(file, indexDirectory)
			payloadReader.writeByFileID(indexList, payload, newDir, newDir, True, targetText)
			os.remove(newDir + os.sep + payload)

	end = time.time()
	print(end - start)


def groupByFileID(payloadDirectory, targetDirectory):
	"""
	uses a directory built by getTextFiles and groups text by 
	"""
	IDlist = []
	name = 0
	paths = glob.glob(payloadDirectory + os.sep + '/*/*') # make / os.sep
	for path in paths:
		ID = os.path.basename(os.path.normpath(path))
		targetDir = targetDirectory  + os.sep + ID
		if ID not in IDlist:
			os.mkdir(targetDir)
			IDlist.append(ID)
		for p, d, f in os.walk(path):
			for filePath in p:
				shutil.copyfile(filePath, targetDir + os.sep + 'payload' + name)
				name += 1


groupByFileID(os.getcwd() + '/javaFiles', '/Users/cssummer16/Documents/summerResearch/blackboxProject/fileIDs')