#Merges SQL query results with state classification file


def mergeData(SQLpath, statesPath):
	# initializes array that will hold eventid, date, user, compilation boolean
	# and state for each compilation in that order
	fullList = []

	states = open(statesPath)
	with open(SQLpath) as table:
		lines = table.readlines()

	#for each compilation event, get relevant data
	for line in lines:
		splitLine = line.split('|')
		master_id = splitLine[1].rstrip()
		event_id = splitLine[2].rstrip()
		is_error = splitLine[3].rstrip()
		message = [splitLine[4].rstrip()]
		created_at = splitLine[5].rstrip()
		# if the line is about a file already added to our full list,
		# just add the error message to the array
		if event_id in fullList[:][0]:
			for x in fullList:
				if x[1] == event_id:
					x[3].append(message)

		# if the file is not yet in the list, add all info as a new item in the array
		else:
			data = getState(event_id, statesPath)
			fullList.append([master_id, event_id, is_error, message, created_at, compiles, state])

	return  fullList




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
				if line[x] == "_":
					underscores += 1

				# Gets compilation result from file name
				if line[x] == "_" and underscores == 4:
					compiles = line[x+1]

				if line[x] == ':':
					colons += 1

				# Gets state from anaylsis.txt
				# .rstrip() removes whitespace & newline chars
				if line[x] == ":" and colons == 2:
					state = line[x:].rstrip()
					break
			break
	#return the compilation result and state of file with given eventid
	return [compiles, state]



def errorsByState(fullList):
	""" takes the full list and makes a dictionary for each for/while loop
	state where the key is the message and the value is the number of files
	with that error message"""
	au

