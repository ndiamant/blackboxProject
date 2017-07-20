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
        eventid =
		is_error =
		date = line[15:97].rstrip()
		data = getState(eventid, statesPath)
		

		

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
