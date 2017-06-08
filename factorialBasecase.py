# blackbox project
# basecase classifier for factorial functions written in Java
import plyj.parser as plyj
from fileGrouper import *
from fileParser import *
from payloadReader import *

parser = plyj.Parser()


def factorialSelector(bbfile):
	""" 
	takes in a java file that contains multiple methods
	if the file contains the function return it
	otherwise return error message
	"""
	fileString = open(bbfile).read()
	facString = ""
	openBrackets = 0
	closeBrackets = 0
	inFunction = False
	for x in range(len(fileString)):
		if fileString[x:x+9] == "factorial":
			inFunction = True
		if inFunction:
			facString += fileString[x]
			if openBrackets == 0 and fileString[x] == ";":
				facString = ""
				inFunction = False
				closeBrackets = 0
			if fileString[x] == "{":
				openBrackets += 1
			elif fileString[x] == "}":
				closeBrackets += 1
			if openBrackets == closeBrackets != 0:
				break
	if inFunction == False:
		print "Factorial method declaration not found in file"
	return "public int " + facString


def makeTree(facString):
	"""
	takes in our string of factorial function and uses plyj to return
	factorial function as a plyj tree
	"""
	return parser.parse_string('public class Foo {' + facString + '}')


def conditionalFinder(facString):
	""" 
	returns a list of tuples containing the type of statement 
	(if, else if or else) and the index at which each statement begins
	"""
	conditionals = []
	x = 0
	while x < len(facString):
		if facString[x:x+7] == "else if":
			conditionals.append(["else if", x])
			x += 7
		elif facString[x:x+4] == "else":
			conditionals.append(["else", x])
			x += 4
		elif facString[x:x+2] == "if":
			conditionals.append(["if", x])
			x += 2
		x += 1
	return conditionals


def conditionalCounter(conditionals):
	"""
	takes in a list of tuples containing the type of conditional and its index
	and turns in into a list of tuples with each containing the type of 
	conditional and the number of times it appears in the code
	"""
	condCount = [["if", 0], ["else if", 0], ["else", 0]]
	for x in range(len(conditionals)):
		if conditionals[x][0] == "if":
			condCount[0][1] += 1
		elif conditionals[x][0] == "else if":
			condCount[1][1] += 1
		elif conditionals[x][0] == "else":
			condCount[2][1] += 1
	return condCount



def defineCase(plyjTree, condCount, facString):
	""" 
	takes in information about the conditionals in a factorial function and
	returns the state that it is classified under
	"""
	if stateSix(facString):
		return "State six"
	elif stateSeven(plyjTree):
		return "State seven"
	elif stateTwo(condCount, plyjTree):
		return "State two"
	elif stateThree(condCount, plyjTree, facString):
		return "State three"
	elif stateFour(condCount, plyjTree):
		return "State four"
	elif stateFive(facString, plyjTree):
		return "State five"
	elif stateOne(facString, condCount, plyjTree):
		return "State one"
	elif stateEight(facString, condCount, plyjTree):
		return "State Eight"
	else:
		return "State Nine"


def stateOne(facString, condCount, plyjTree):
	"""
	checks if program is in State 1 (the base case is correct)
	returns true if the State 1 criteria are met, false otherwise
	"""
	if condCount[0][1] != 1 or condCount[1][1] != 0 or condCount[2][1] != 1 or not recursiveMethodFinder(plyjTree)[0]:
		return False
	listOfArgs = getArgs(facString)

	if len(listOfArgs) != 1:
			return False
	else:
		# testing for the possible correct basecase eqaulities and inequalities
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
		elif listOfArgs[0] + "<=0" in facString.replace(" ", ""):
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
		 and not stateOne(facString, condCount, plyjTree) and not stateFive(facString, plyjTree) and recursiveMethodFinder(plyjTree)[0])


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

	# Check to see if factorial argument is changed before or during recursive call
	if recursiveMethodFinder(plyjTree)[0]:
		if len(listOfArgs) == 1:
			if listOfArgs[0] + "-1" in facString.replace(" ", ""):
				return False
		else:
			return True
	return False


def stateSix(facString):
	""" 
	check if program is in State 6 by looking for
	evidence of for or while loops
	"""
	for x in range(len(facString)-1):
		if facString[x:x+3] == "for":
			return True
		elif facString[x:x+5] == "while":
			return True
	return False


def stateSeven(plyjTree):
	"""
	checks if program is using tail recursion by looking for a call
	to a function that is not itself
	"""
	if checkInstance(plyjTree, plyj.MethodDeclaration)[0] and not recursiveMethodFinder(plyjTree)[0]:
		return True
	return False
	# TODO: try to analyze function that is called
	# TODO: check the number of arguments in function that is called

def stateEight(facString, condCount, plyjTree):
	"""
	check if program is using ternary operator by looking if the code string
	contains colons and question marks
	"""
	if condCount[0][1] == 0 and condCount[1][1] == 0 and condCount[2][1] == 0 and ':' in facString and '?' in facString and recursiveMethodFinder(plyjTree)[0]:
		return True
	return False


def getArgs(facString):
	"""
	helper function that extracts the name of the argument
	passed into the factorial function
	"""
	# loop through function to extract parameters
	start = 0
	end = 0
	for i in range(len(facString)):
		if facString[i] == '(':
			start = i
		elif facString[i] == ')':
			end = i
			break;
	args = facString[start+1: end]
	# remove types from argument names
	args = args.replace("byte", "")
	args = args.replace("char", "")
	args = args.replace("short", "")
	args = args.replace("int", "")
	args = args.replace("long", "")
	args = args.replace("float", "")
	args = args.replace("double", "")
	args = args.replace(" ", "")
	# return argument names as a list
	return args.split(',')



