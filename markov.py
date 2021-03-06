from collections import defaultdict
import numpy as np
import fileParser
import itertools
import payloadReader
import contextlib
import sys

def transitionFreq(textList):
        """
        returns a dictionary keyed with a line count with a value of
        a np array with the number of transitions to all of the other states
        labelled by labels
        """
        textList = sorted(textList, key = lambda entry: entry[1][0])
        lengths = map(lambda entry: countLines(entry[0]), textList)
        labels = range(0, max(lengths) + 1)
        transDict = defaultdict(lambda: np.array([0] * (max(lengths) + 1)))
        counter = 0
        # key is the file ID, group is an iterable of the all the entries corresponding to the key
        for key, group in itertools.groupby(textList, lambda entry: entry[1][0]):
                length = len(list(group))
                for index in xrange(1, length - 1):     # maybe should be (0, length -1)          
                        following = lengths[index + 1 + counter]
                        transDict[lengths[index + counter]][following] += 1
                counter += length
        return transDict, labels


def generalMarkov(textList, stateFunc, order = 1, states = []):
        """
        Takes a textList in payloadReader's textList format, a stateFunc that takes 
        an entry of a textList and finds the state in a Markov model it belongs to, the 
        order of the markov model, and optionally a list of the states that each entry in
        the textList belongs to. STATES MUST BE IN THE ORDER OF sorted(textList, key = lambda entry: entry[1][0]).
        Returns an _order_+1 dimensional array where the first dimension is the first state, then indexing into 
        the next _order_ dimensions will give the number of transtions from the first state to the indexed state. 
        In a first order heat map, row is from state, column is to state, color is frequency of transition.
        """   
        # order the text list for fileID grouping
        textList = sorted(textList, key = lambda entry: entry[1][0])
        # find the state of each file so that only has to be done once for each
        if not states:
                states = map(stateFunc, textList)
        # label for each state
        stateLabels = sorted(list(set(states)))
        # create the order-dimensional list of states 
        numStates = len(stateLabels)
        transArray = np.zeros((numStates,) * (order + 1))
        # an iterator to know where to index into states
        counter = 0      
        # key is the file ID, group is an iterable of the all the entries corresponding to the key
        for key, group in itertools.groupby(textList, lambda entry: entry[1][0]):
                # length of a group to keep track of the number of files iterated through
                length = len(list(group))
                # loop through items of group
                for index in xrange(0, length - order):               
                        # find the states transitioned to
                        state = []
                        # first state transitioned to is row, next is column, etc.
                        for step in xrange(0, order):
                                state.append(stateLabels.index(states[index + step + counter + 1]))
                        # index using the state and update transDict
                        transArray[stateLabels.index(states[index + counter])][tuple(state)] += 1
                counter += length
        return transArray, stateLabels



def testFunc(text):
        if 'printAuthor' in text: 
                return 1
        elif 'printTitle' in text:
                return 2
        elif 'getPages' in text:
                return 3
        elif 'printDetails' in text:
                return 4
        elif 'setRefNumber' in text:
                return 5
        elif 'getRefNumber' in text:
                return 6
        else: 
                return 0    

def laplaceSmooth(vector, k = 1):
        """
        laplace smooth a n by 1 vector with constant k
        """
        total = float(sum(vector))
        return map(lambda entry: (entry + k)/(total + k * len(vector)), vector)


def printDetailsState(text):
        """ 
        before passing to this method, filter the textList as follows:
        textList = filter(lambda x: 'printDetails' in x[0], textList)
        """
        state = 0
        try:
                tree = fileParser.parser.parse_string(text)
        except Exception:
                return 0
        tree = fileParser.methodFinder(tree, 'printDetails')[1]
        if equal(tree, 'return_type', 'void'):
                state = 1
                if tree.parameters == []:
                        state = 2
                        tree = tree.body
                        if tree:
                                expressionStatements = filter(lambda x: isinstance(x, fileParser.plyj.ExpressionStatement), tree)
                                statesPresent = [False, False, False] # prints author, prints title, prints pages
                                for expressionStatement in expressionStatements:
                                        expression = expressionStatement.expression
                                        if equal(expression, 'name', 'println') or equal(expression, 'name', 'print'):
                                                if fileParser.findGoal(expression.arguments, str, 'author')[0]:
                                                        statesPresent[0] = True
                                                if fileParser.findGoal(expression.arguments, str, 'title')[0]:
                                                        statesPresent[1] = True
                                                if fileParser.findGoal(expression.arguments, str, 'pages')[0]:
                                                        statesPresent[2] = True
                                # binary coding of all combinations of author, title, pages
                                state += int(statesPresent[0]) + 2 * int(statesPresent[1]) + 4 * int(statesPresent[2]) 
        return state
        # printDetailsLine = text.split('\n')
        # printDetailsLine = filter(lambda line: 'printDetails' in line, printDetailsLine)
        # printDetailsText = printDetailsLine[0] + re.search('(.*)printDetails\(.*\)\{(.*)\}', text, re.DOTALL).group(2)
        # print printDetailsText


def equal(a, attr, b):
        try:
                if getattr(a, attr) == b:
                        return True
        except Exception:
                return False


def printDetailsState2(text):
        """
        257 states possible 
        """
        # each part of the method is either present (1) or not (0)
        states = [0] * 9
        tree = fileParser.parser.parse_string(text)
        # check if compiles
        if tree:
                states[0] = 1
        else:
                return states
        # tree is now the AST (abstract syntax tree) of printDetails
        tree = fileParser.methodFinder(tree, 'printDetails')[1]
        # correct return type?
        if equal(tree, 'return_type', 'void'):
                states[1] = 1
        # correct params?
        if equal(tree, 'parameters', []):
                states[2] = 1
        # tree is now AST of the body of printDetails
        try:
                tree = tree.body
        except Exception:
                return states
        if tree:
                expressionStatements = filter(lambda x: isinstance(x, fileParser.plyj.ExpressionStatement), tree)
                for expressionStatement in expressionStatements:
                        expression = expressionStatement.expression
                        # check if prints author, title, pages
                        if equal(expression, 'name', 'println') or equal(expression, 'name', 'print'):
                                if fileParser.findGoal(expression.arguments, str, 'author')[0]:
                                        states[3] = 1
                                if fileParser.findGoal(expression.arguments, str, 'title')[0]:
                                        states[4] = 1
                                if fileParser.findGoal(expression.arguments, str, 'pages')[0]:
                                        states[5] = 1
                ifStatements = filter(lambda x: isinstance(x, fileParser.plyj.IfThenElse), tree)
                # check if if statement present
                if ifStatements:
                        states[6] = 1

                lengthIf = fileParser.methodInvocationFinder(ifStatements, 'length')
                # check if length is called on refNumber 
                if lengthIf[0] and equal(lengthIf[1].target, 'value', 'refNumber'):
                        states[7] = 1
                # check if ifStatements contain 'zzz'
                if fileParser.findGoal(ifStatements, str, 'zzz')[0]:
                        states[8] = 1

        return states

 
def reduceStates(states):
        """
        0 = no compile 
        1 = correct return type (void) and no arguments 
        2 = not 1 but prints correct things
        3 = 1 and 2
        4 = not 1 or 2, but correct if statement
        5 = 1 and 4 but not 2
        6 = 2 and 4 but not 1
        7 = method complete
        """
        return states[1] * states[2] + 2 * states[3] * states[4] * states[5] + 4 * states[6] * states[7] * states[8]


def walk(currentState, probMat):
        """
        given the current state, go to a random state determined by the probabilities
        in probabilityMat
        """
        return np.random.choice(probMat.shape[0], p = probMat[currentState])


def meanDistToCompletion(state, probMat, iterations):
        """
        Uses Monte Carlo simulation to estimate the number of iterations required 
        to go from a state to the completion state. Assumes once complete, stays complete.
        """
        dists = []
        for i in xrange(iterations):
                curState = state
                dist = 0
                while not curState == probMat.shape[0] - 1:
                        curState = walk(curState, probMat)
                        dist += 1
                dists.append(dist)
        return sum(dists) / len(dists)


def mutualInformation(arr, k = 1):
        """
        measures the pointwise mutual information between all 
        of the values in arr. arr should be structured like this:
        array([[1, 1, 1, ..., 1, 1, 1],
        [1, 1, 1, ..., 1, 1, 1],
        [1, 1, 1, ..., 1, 1, 1],
        ..., 
        [1, 1, 1, ..., 0, 0, 0],
        [1, 1, 1, ..., 0, 0, 0],
        [1, 1, 1, ..., 0, 0, 0]])
        k makes this PMI^k 
        See HANDLING THE IMPACT OF LOW FREQUENCY EVENTS 
        ON CO-OCCURRENCE BASED MEASURES OF WORD SIMILARITY KDIR 2011
        for analysis
        """
        totals = sum(arr)
        mutualInfo = np.zeros((arr.shape[1], arr.shape[1]))
        for i in xrange(arr.shape[1]):
                for j in xrange(i):
                        # mutualInfo[i][j] = len(filter(lambda v: v[i] == v[j], arr)) / float(totals[i] * totals[j]) * arr.shape[0]
                        mutualInfo[i][j] = (float(len(filter(lambda v: v[i] == v[j], arr))) / arr.shape[0])**k / (float(totals[i]) * totals[j] / arr.shape[0]**2)


        return np.log2(mutualInfo)


def printDetailsState3(textList):
        """
        As opposed to the previous state functions, printDetailsState3 
        takes a whole textList and generates the states for the optional fourth
        argument in generalMarkov.
        """
        textList = sorted(textList, key = lambda entry: entry[1][0])
        errList = fileParser.getErrMessages(textList, 'uniqueNameTemp', 'Book.java')
        errList = fileParser.parseErrors(errList)
        states = []
        for err, entry in itertools.izip(errList, textList):
                if err: # is there a compiler error?
                        methodLine = fileParser.getMethodLines('printDetails', entry[0])
                        print methodLine
                        if methodLine[0] <= err[0] <= methodLine[1]: # is the error in our method?
                                states.append(err[1])
                        else:
                                states.append(0) # if not return the code for does not compile
                else:
                        states.append(reduceStates(printDetailsState2(entry[0]))) # if there is no error, find which non-error state the entry belongs to
        return states
######################## Taken from Alex Martinelli on stack overflow #########################
class DummyFile(object):
        def write(self, x): pass

@contextlib.contextmanager
def nostdout():
        save_stdout = sys.stdout
        sys.stdout = DummyFile()
        yield
        sys.stdout = save_stdout
##############################################################################################
import pickle
import time
with open('tld.txt') as f:
        tld = pickle.load(f)
def writeErrs(start, end, name = 'uniqueNameTemp'):
        t0 = time.time()
        errList = fileParser.getErrMessages(tld[start:end], name, 'Book.java')
        errList = fileParser.parseErrors(errList)
        print time.time() - t0Mr
        pickle.dump(errList, open('err'+str(start)+'-'+str(end)+'.p', 'wb'))
        return errList

s = writeErrs(0,10)
print s
