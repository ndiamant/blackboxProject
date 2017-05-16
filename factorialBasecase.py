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
	for x in len(bbfile):
		if bbfile[x:x+9] == "factorial":
			inFunction = true
			x += 1
		if inFunction:
			facString += bbfile[x]
			if bbfile[x] == "{":
				openBrackets += 1
			if bbfile[x] == "}":
				closeBrackets -= 1
			if openBrackets == closeBrackets != 0:
				break
		else:
			x += 1
	print "Factorial method declaration not found in file"
	return ""


def treeSelector(bbfile):
	"""
	takes in our file name and uses plyj to return
	factorial function in the file as a plyj tree
	returns error message if the method cannot be called
	"""
	if 'fac' not in open(bbfile).read() and 'factorial' not in open(bbfile).read():	
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
	if stateOne(conditionals, condCount) and recursiveMethodFinder(plyjTree):
		return "State one"
	elif stateTwo(conditionals, condCount) and recursiveMethodFinder(plyjTree):
		return "State two"
	elif stateThree(conditionals, condCount) and recursiveMethodFinder(plyjTree):
		return "State three"
	elif stateFour(conditionals, condCount) and recursiveMethodFinder(plyjTree):
		return stateFourType(textfile, conditionals, condCount, plyjTree)
	else:
		return "Case not covered in potential states"


def stateOne(textfile, conditionals, condCount):
	"""
	checks if program is in State 1 (the base case is correct)
	returns true if the State 1 criteria are met, false otherwise
	"""
	if condCount[0][1] != 1 or condCount[1][1] != 0 or condCount[2][1] != 1:
		return false
	else:
		#TODO determine if basecase is correct
		return "TODO"
		

def stateTwo(conditionals, condCount):
	"""
	checks if program is in State 2 (redundant basecase)
	returns true if the State 2 criteria are met, false otherwise
	"""
	return (condCount[0][1] > 1 or condCount[1][1] > 0)


def stateThree(conditionals, condCount):
	"""
	checks if program is in State 3 (base case structured properly but incorrect)
	returns true if the State 3 criteria are met, false otherwise
	"""
	return (condCount[0][1] == 1 and condCount[1][1] == 0 and condCount[2][1] == 1)
		 #and !stateOne)


def stateFour(conditionals, condCount):
	"""
	checks if program is in State 4 (no base case)
	returns true if the State 4 criteria are met, false otherwise
	"""
	return (condCount[0][1] == 0 and condCount[1][1] == 0 and condCount[2][1] == 0)


def stateFourType(textfile, conditionals, condCount, plyjTree):
	"""
	given the conditionals and condCount for a function already
	determined to be in State 4, determines a more specific state
	for the given function using the following criteria:
		4A: Has no base case, but does have a recursive step
		4B: Has no base case and uses a for or while loop
		4C: Has no base case and no method implemented
	"""
	if condCount[0][1] != 0 or condCount[1][1] != 0 or condCount[2][1] != 0:
		return "program is not in state 4"

	#check 4A by looking for recursive step
	elif recursiveMethodFinder(plyjTree):
		return "State 4A"

	#check 4B by looking for for or while loop
	for x in range(len(textfile)-1):
		if textfile[x:x+2] == "for":
			return "State 4B"
		elif textfile[x:x+4] == "while":
			return "State 4B"
		else:
			x += 1

	#if in state 4, but not 4A or 4B, it must be in state 4C
	return "State 4C"


