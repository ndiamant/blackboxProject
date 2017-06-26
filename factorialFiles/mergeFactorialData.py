#Merges SQL query results with state classification file


def mergeData(SQLpath, statesPath):
	# initialize dictionary which will hold userids as keys and states 
	# (in compilation order) as values
	dic = {}

	# initializes array that will hold eventid, date, user, compilation boolean
	# and state for each compilation in that order
	fullList = []

	states = open(statesPath)
	with open(SQLpath) as table:
		lines = table.readlines()

	#for each compilation event, get relevant data
	for line in lines:
		eventid = line[2:12]
		date = line[15:97].rstrip()
		user = line[100:107]
		data = getState(eventid, statesPath)
		compiles = data[0]
		state = numericState(data[1])

		# add state as value to dic where user is the key
		if user in dic:
			dic[user] += [state]
		else:
			dic[user] = [state]

		# add all data to array
		fullList.append([eventid, date, user, compiles, state])

	return dic, fullList




def getState(eventid, statesPath):
	file = open(statesPath)
	states = file.readlines()
	compiles = ""
	state = ""
	for line in states:
		if eventid in line:
			underscores = 0
			for x in range(len(line)):
				if line[x] == "_":
					underscores += 1

				# Gets compilation result from file name
				if line[x] == "_" and underscores == 4:
					compiles = line[x+1]

				# Gets state from anaylsis.txt
				# .rstrip() removes whitespace & newline chars
				if line[x] == "S":
					state = line[x:].rstrip()
					break
			break
	#return the compilation result and state of file with given eventid
	return [compiles, state]


def numericState(state):
	#takes text string of state and turns state into integer
	if "one" in state:
		return 1
	elif "two" in state:
		return 2
	elif "three" in state:
		return 3
	elif "four" in state:
		return 4
	elif "five" in state:
		return 5
	elif "six" in state:
		return 6
	elif "seven" in state:
		return 7
	elif "Eight" in state:
		return 8
	elif "Nine" in state:
		return 9
	# if file does not have factorial function declaration, give it a state of 0
	else:
		return 0


