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

	#return flatFileList
	for l in fileList:
		if '.DS_Store' in l:
			l.remove('.DS_Store')
	result = []
	for l in fileList:
		if l != []:
			result.append(l)

	#return result
	return homePath, subDirList, result, flatFileList


"""
run the case analysis on all the java files and store the results
in analysis.txt file 
"""
def getCases(fileList):
	caseDict = {}
	categoryDict = {"State one": 0, "State two": 0, "State three": 0, 
					"State four": 0, "State five": 0, "State six": 0,
					"State seven": 0, "State eight": 0, "State nine": 0}
	#for l in fileList:
	#	for fileName in l:
	#		fac = factorialSelector(fileName)
	#		tree = makeTree(fac)
	#		cond = conditionalFinder(fac)
	#		condCount = conditionalCounter(cond)
	#		case = defineCase(tree, condCount, fac)
	#		caseDict[fileName] = case
	success = 0
	record = 0
	total = len(flatFileList)

	for directory in subDirList[1:]:
		os.chdir(directory)
		for dirpath, dirnames, filenames in os.walk(directory):
			for fileName in filenames:
				fac = factorialSelector(fileName)
				if fac != "":
					tree = makeTree(fac)
					cond = conditionalFinder(fac)
					condCount = conditionalCounter(cond)
					case = defineCase(tree, condCount, fac)
					caseDict[fileName] = case
					if case == "State one":
						categoryDict["State one"] += 1
					elif case == "State two":
						categoryDict["State two"] += 1
					elif case == "State three":
						categoryDict["State three"] += 1
					elif case == "State four":
						categoryDict["State four"] += 1
					elif case == "State five":
						categoryDict["State five"] += 1
					elif case == "State six":
						categoryDict["State six"] += 1
					elif case == "State seven":
						categoryDict["State seven"] += 1
					elif case == "State eight":
						categoryDict["State eight"] += 1
					elif case == "State nine":
						categoryDict["State nine"] += 1

	success = len(caseDict)

	os.chdir('/Users/cssummer17/Desktop/CSTT/blackboxProject')
	with open("analysis.txt", "a+") as f:
			f.write(str(success) + "/" + str(total) + '\n')
	for key in caseDict:
		with open("analysis.txt", "a+") as f:
			record += 1
			f.write(str(record) + ': ' + key + ": " + caseDict[key] + '\n')

	for key in categoryDict:
		with open("percentage.txt", "a+") as f:
			f.write(key + ": " + str(categoryDict[key]*100.0/total) + "%" + '\n')

	for key in categoryDict:
		with open("percentage2.txt", "a+") as f:
			f.write(key + ": " + str(categoryDict[key]*100.0/success) + "%" + '\n')