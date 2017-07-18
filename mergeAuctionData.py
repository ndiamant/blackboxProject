#Merges SQL query results with state classification file



""" takes in data from mySQL queries as well as a list of file names
	and their corresponding states
	returns dataList, a 2D array that includes the id, error boolean, 
	compilation message, compilation boolean and state for each file 
"""
def mergeData(SQLpath, statesPath):

	# initializes array that will hold eventid, is_error, message, compilation boolean
	# and state for each compilation in that order
	dataList = []

	states = open(statesPath)
	with open(SQLpath) as table:
		lines = table.readlines()

	#for each compilation event, get relevant data
	for line in lines:
		eventid = line[2:12]
		is_error = line[14:24]
		message = line[26:]
		data = getState(eventid, statesPath)
		compiles = data[0]
		state = data[1]

		# add all data to array
		dataList.append([eventid, is_error, message, compiles, state])

	return dataList



""" gets compile boolean and state from state classifier data
	by identifying the file with the given event_id and extracting
	the state of the file
"""
def getState(eventid, statesPath):
	file = open(statesPath)
	states = file.readlines()
	compiles = ""
	state = ""
	for line in states:
		if eventid in line:
			underscores = 0
			colons = 0
			for x in range(len(line)):
				# Gets compilation result from file name
				if line[x] == "_":
					underscores += 1
					if underscores == 4:
						compiles = line[x+1]

				elif line[x] == ":":
					colons += 1

				# Gets state from anaylsis.txt
				# .rstrip() removes whitespace & newline chars
				if line[x] == ":":
					colons += 1
					if colons == 2:
						state = line[x+1:].rstrip()
						break
			break
	#return the compilation result and state of file with given eventid
	return [compiles, state]



""" takes in a list of data and uses it to make 5 dictionaries of the
	form key = error message, value = number of occurances
	The five dictionaries are a general dictionary and then one 
	dictionary each for the four states (for, while, both, neither)

	The frequency dics can then be used to show the relative error
	frequencies for functions in each state
"""
def errorFreq(dataList):
	#initialize dictionary for all files and dictionaries for each state
	freqDic = {}
	forFreqDic = {}
	whileFreqDic = {}
	bothFreqDic = {}
	neitherFreqDic = {}

	#add to frequency of error message count for appropriate dictionaries
	for x in fullList:
		message = fullList[x][2]
		state = fullList[x][4]
		addToDic(freqDic, message)
		if state == 'for':
			addToDic(forFreqDic, message)
		elif state == 'while':
			addToDic(whileFreqDic, message)
		elif state == 'both':
			addToDic(bothFreqDic, message)
		elif state == 'neither':
			addToDic(neitherFreqDic, message)

	return freqDic, forFreqDic, whileFreqDic, bothFreqDic, neitherFreqDic

""" 
	takes an item, item, and adds it to a dictionary, dic
	helper function for the errorFreq function
"""
def addToDic(dic, item):
	if item in dic:
		current = dic[item]
		dic[item] = current + 1
	else:
		dic[item] = 1 
	return dic


"""
	takes in a frequency dictionary and changes the value
	of each key from a count of occurances of that key to 
	a percent of occurances of that key
"""
def makeRelFreq(dic):
	total = 0

	#add values in dic to get total number
	for key in dic:
		total += dic[key] 
	for key in dic:
		dic[key] = float(dic[key])/float(total)
	return dic


"""
	Creates a list of list based on 5 frequency dictionaries
	Each inner list with have a length of 6 with the form
	[error message, percent of files in dic1 w/ message,
	percent in dic2, percent in dic3, percent in dic4, 
	percent in dic5] 
	Using the outputs from error freq, this function 
	allows us to look at the distribution of error messages
	across file states
"""
def freqTable(dic1, dic2, dic3, dic4, dic5):
	dic1 = makeRelFreq(dic1)
	dic2 = makeRelFreq(dic2)
	dic3 = makeRelFreq(dic3)
	dic4 = makeRelFreq(dic4)
	dic5 =makeRelFreq(dic5)
	table = []
	
	for key in dic1:
		error = [key, dic1[key], dic2[key], 
			dic3[key], dic4[key], dic5[key]]
		table += error
	return table









