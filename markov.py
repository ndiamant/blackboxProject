### IGNORE THIS FILE FOR NOW ###


from collections import defaultdict
import numpy as np
import fileParser
import itertools

def countLines(text):
        return text.count('\n')


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


def generalMarkov(textList, stateFunc, order = 1):
        """
        returns a dictionary keyed with states and valued with numpy
        arrays with the number of transitions to all of the other states
        labelled by labels
        """   
        # order the text list for fileID grouping
        textList = sorted(textList, key = lambda entry: entry[1][0])
        # find the state of each file so that only has to be done once for each
        states = map(stateFunc, textList)
        # find all of the possible state combinations and put in a static order 
        if order == 1:
                labels = stateLabels = sorted(list(set(states)))
        else:
                labels = sorted(list(itertools.combinations_with_replacement(set(states), order)))
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
                        # index using the state and updat transDict
                        transArray[stateLabels.index(states[index + counter])][tuple(state)] += 1
                counter += length
        return transArray, labels



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

def laplaceSmooth(vector, k):
        """
        laplace smooth a n by 1 vector with constant k
        """
        total = float(sum(vector))
        return map(lambda entry: (entry + k)/(total + k * len(vector)), vector)

