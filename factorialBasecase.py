# blackbox project
# basecase identifier
import plyj.parser as plyj


def factorialSelector(bbfile):
	""" 
	takes in a java file that contains multiple methods
	if the file contains the function return it
	otherwise return error message
	"""
	facString = ""
	openBrackets = 0
	closeBrackets = 0
	inFunction = false
	for x in range(len(bbfile)):
		if bbfile[x:x+9] == "factorial":
			inFunction = true
		if inFunction:
			facString += bbfile[x]
			if bbfile[x] == "{":
				openBrackets += 1
			elif bbfile[x] == "}":
				closeBrackets += 1
			if openBrackets == closeBrackets != 0:
				break
	#print "Factorial method declaration not found in file"
	return facString


def treeSelector(bbfile):
	"""
	takes in our file name and uses plyj to return
	factorial function in the file as a plyj tree
	returns error message if the method cannot be called
	"""
	if 'factorial' not in open(bbfile).read():	
		print "Factorial Function does not exist in this file" 
		return None
	else:
		parser = plyj.Parser()
		return parser.parse_file(file(bbfile))


def conditionalFinder(facString):
	""" 
	returns a list of tuples containing the type of statement 
	(if, else if or else) and the index at which each statement begins
	"""
	conditionals = []
	x = 0
	while x < len(facString):
		if textfile[x:x+7] == "else if":
			conditionals += ("else if", x)
			x += 7
		elif textfile[x:x+4] == "else":
			conditionals += ("else", x)
			x += 4
		elif textfile[x:x+2] == "if":
			conditionals += ("if", x)
			x += 2
		x += 1
	return conditionals


def conditionalCounter(conditionals):
	"""
	takes in a list of tuples containing the type of conditional and its index
	and turns in into a list of tuples with each containing the type of 
	conditional and the number of times it appears in the code
	"""
	condCount = [("if", 0), ("else if", 0), ("else", 0)]
	for x in range(len(conditionals)):
		if conditionals[x][0] == "if":
			condCount[0][1] += 1
		elif conditionals[x][0] == "else if":
			condCount[1][1] += 1
		elif conditionals[x][0] == "else":
			condCount[2][1] += 1
	return condCount


def defineCase(plyjTree, conditionals, condCount):
	""" 
	takes in information about the conditionals in a factorial function and
	returns a state based on the accuracy of the if statement written
	"""
	if stateOne(facString, condCount, plyjTree):
		return "State one"
	elif stateTwo(condCount, plyjTree):
		return "State two"
	elif stateThree(condCount, plyjTree, facString):
		return "State three"
	elif stateFour(condCount, plyjTree):
		return "State four"
	elif stateFive(facString, plyjTree):
		return "State five"
	elif stateSix(facString):
		return "State six"
	else:
		return "State seven"


def stateOne(facString, condCount, plyjTree):
	"""
	checks if program is in State 1 (the base case is correct)
	returns true if the State 1 criteria are met, false otherwise
	"""
	if condCount[0][1] != 1 or condCount[1][1] != 0 or condCount[2][1] != 1 or !recursiveMethodFinder(plyjTree)[0]:
		return False
	listOfArgs = getArgs(facString)ß
	if len(listOfArgs) != 1:
			return False
	else:
		if listOfArgs[0] + "==1" in facString.replace(" ", ""):
			return True
		elif listOfArgs[0] + "==0" in facString.replace(" ", ""):
			return True
		elif listOfArgs[0] + "<1" in facString.replace(" ", ""):
			return True
		elif listOfArgs[0] + "<=1" in facString.replace(" ", ""):
			return True
		elif listOfArgs[0] + "<2" in facString.replace(" ", ""):
			return True
		elif listOfArgs[0] + "!>1" in facString.replace(" ", ""):
			return True
		elif listOfArgs[0] + "!>2" in facString.replace(" ", ""):
			return True
	return False


		

def stateTwo(condCount, plyjTree):
	"""
	checks if program is in State 2 (redundant basecase)
	returns true if the State 2 criteria are met, false otherwise
	"""
	return ((condCount[0][1] > 1 or condCount[1][1] > 0) and recursiveMethodFinder(plyjTree))


def stateThree(condCount, plyjTree, facString):
	"""
	checks if program is in State 3 (base case structured properly but incorrect)
	returns true if the State 3 criteria are met, false otherwise
	"""
	return (condCount[0][1] == 1 and condCount[1][1] == 0 and condCount[2][1] == 1
		 and !stateOne(facString, condCount) and !stateFive(facString, plyjTree) and recursiveMethodFinder(plyjTree)[0])


def stateFour(condCount, plyjTree):
	"""
	checks if program is in State 4 (no base case)
	returns true if the State 4 criteria are met, false otherwise
	"""
	return (condCount[1][1] == 0 and condCount[2][1] == 0 and
		recursiveMethodFinder(plyjTree)[0]) 

def stateFive(facString, plyjTree):
	"""
	check is program is in state 5, meaning that there is a basecase
	implemented, but it is not reachable
	"""
	listOfArgs = getArgs(facString)

	if recursiveMethodFinder(plyjTree)[0]:
		if len(listOfArgs) == 1:
			if listOfArgs[0] + "-1" in facString.replace(" ", ""):
				return False
		elif len(listOfArgs) == 2:
			#TODO
			#Maybe tail recursion
			...
		else:
			return True
	return False


def stateSix(facString):
	""" 
	check if program is in State 6 by looking for
	evidence of for or while loops
	"""
	for x in range(len(facString)-1):
		if facString[x:x+2] == "for":
			return True
		elif facString[x:x+4] == "while":
			return True
	return False


def getArgs(facString):
	"""
	helper function that extracts the name of the argument
	passed into the factorial function
	"""
	start = 0
	end = 0
	for i in range(len(facString)):
		if facString[i] == '(':
			start = i
		elif facString[i] == ')':
			end = i
	args = facString[start+1: end]
	args = args.replace("byte", "")
	args = args.replace("char", "")
	args = args.replace("short", "")
	args = args.replace("int", "")
	args = args.replace("long", "")
	args = args.replace("float", "")
	args = args.replace("double", "")
	args = args.replace(" ", "")
	return args.split(',')



