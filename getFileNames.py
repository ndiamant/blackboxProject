import os
from factorialBasecase import *

def getFileNames():
	fileList = []
	subDirList = []
	#path = '/Users/cssummer17/Desktop/abc'
	path = '/Users/cssummer17/Desktop/CSTT/blackboxProject/javaFiles'
	for dirpath, dirnames, filenames in os.walk(path):
		fileList.append(filenames)
		#print dirpath
		subDirList.append(dirpath)
	#flatFileList = [item for sublist in fileList for item in sublist]
	#flatFileList[:] = [x for x in flatFileList if x != '.DS_Store']
	#return flatFileList
	#for l in fileList:
	#	if '.DS_Store' in l:
	#		l.remove('.DS_Store')
	#result = []
	#for l in fileList:
	#	if l != []:
	#		result.append(l)
	#return result


def getCases(fileList):
	caseDict = {}
	for l in fileList:
		for fileName in l:
			fac = factorialSelector(fileName)
			tree = makeTree(fac)
			cond = conditionalFinder(fac)
			condCount = conditionalCounter(cond)
			case = defineCase(tree, condCount, fac)
			caseDict[fileName] = case
	for key in caseDict:
		with open("analysis.txt", "a+") as f:
			f.write(key + ": " + caseDict[key])