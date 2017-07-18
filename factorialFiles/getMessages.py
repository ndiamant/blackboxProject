
def stripMessages(file):
	"""creates 5 dictionaries for all files, for loop files,
	while loop files, both for and while loop files, and the
	files wth neither to show the ferquency of errors in each 
	"""
	forDic, whileDic, bothDic, neitherDic, allDic = {}

	file = file.open()
	read = file.readlines()
	for line in read:
		split = line.split()
		message = split[5]
		masterid = split[1]
		state = getState(masterid)
		if state == 'for':
			addToDic(message, dic)
		




def addToDic(message, dic):
	if message in dic:
			dic[message] += 1
		else:
			dic[message] = 1


def getState(masterid):
