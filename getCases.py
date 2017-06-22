import os
from factorialBasecase import *


"""
get the names of the java files that are to be analyzed 
"""
def getFileNames():
	fileList = []
	subDirList = []
	#path = '/Users/cssummer17/Desktop/abc'
	path = '/Volumes/Seagate/allfiles/javafiles'
	for dirpath, dirnames, filenames in os.walk(path):
		fileList.append(filenames)
		#print dirpath
		subDirList.append(dirpath)
	flatFileList = [item for sublist in fileList for item in sublist]
	flatFileList[:] = [x for x in flatFileList if x != '.DS_Store']
	return flatFileList
	#for l in fileList:
	#	if '.DS_Store' in l:
	#		l.remove('.DS_Store')
	#result = []
	#for l in fileList:
	#	if l != []:
	#		result.append(l)
	#return result


"""
run the case analysis on all the java files and store the results
in analysis.txt file 
"""
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