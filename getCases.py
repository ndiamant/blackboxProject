import os
from factorialBasecase import *

def getFileNames():
	"""
	get the names of the java files that are to be analyzed 
	"""
	fileList = []
	subDirList = []
	#path = '/Users/cssummer17/Desktop/abc'
	homePath = '/Users/cssummer17/Desktop/CSTT/blackboxProject/javaFiles'
	for dirpath, dirnames, filenames in os.walk(homePath):
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
	return homePath, subDirList


def getCases():
	"""
	run the case analysis on all the java files and store the results
	in analysis.txt file 
	"""
	homePath, subDirList = getFileNames()
	caseDict = {}
	#for l in fileList:
	#	for fileName in l:
	#		fac = factorialSelector(fileName)
	#		tree = makeTree(fac)
	#		cond = conditionalFinder(fac)
	#		condCount = conditionalCounter(cond)
	#		case = defineCase(tree, condCount, fac)
	#		caseDict[fileName] = case

	for directory in subDirList[1:]:
		os.chdir(directory)
		for dirpath, dirnames, filenames in os.walk(directory):
			for fileName in filenames:
				print fileName
				fac = factorialSelector(fileName)
				tree = makeTree(fac)
				cond = conditionalFinder(fac)
				condCount = conditionalCounter(cond)
				case = defineCase(tree, condCount, fac)
				caseDict[fileName] = case

	os.chdir(homePath)
	for key in caseDict:
		with open("analysis.txt", "a+") as f:
			f.write(key + ": " + caseDict[key] + '\n')