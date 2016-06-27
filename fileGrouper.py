import os
import payloadReader

def getTextFiles(indexDirectory, targetDirectory, targetText, userName):
	"""
	Assumes index files are in the format found on the white box server. 
	"""
	for p, d, f in os.walk(indexDirectory): # path, directories, files
		f = filter(lambda x: "index" in x, f) # make sure only using index files
		for file in f:
			newDir = targetDirectory + os.sep + file[6:]
			payload = 'payload-' + file[6:]
			os.mkdir(newDir)
			scpCommand = 'scp ' + 'userName' + '@white.kent.ac.uk:/data/compile-inputs/' + payload + ' ' + newDir
			os.system(scpCommand)
			indexList = payloadReader.createIndexList(file, indexDirectory)
			payloadReader.writeByFileID(indexList, payload, newDir, newDir, True, targetText)
			os.remove(newDir + os.sep + payload)