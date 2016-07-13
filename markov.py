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
        labels = sorted(list(itertools.combinations_with_replacement(set(states), order)))
        # label for each state
        stateLabels = sorted(list(set(states)))
        # create the order-dimensional list of states 
        defaultList = [0]
        numStates = len(stateLabels)
        for i in xrange(order):
                defaultList = [numStates * defaultList]
        defaultList = defaultList[0]
        # create the transition dictionary using defaultList
        transDict = defaultdict(lambda: np.array(defaultList))       
        # an iterator to know where to index into states
        counter = 0      
        # key is the file ID, group is an iterable of the all the entries corresponding to the key
        for key, group in itertools.groupby(textList, lambda entry: entry[1][0]):
                # length of a group to keep track of the number of files iterated through
                length = len(list(group))
                # loop through items of group
                for index in xrange(0, length - order):               
                        # find the state a 
                        state = []
                        for step in xrange(0, order):
                                state.append(stateLabels.index(states[index + step + counter + 1]))
                        # index using the state and updat transDict
                        transDict[states[index + counter]][tuple(state)] += 1
                        # print state
                        # print len(states)
                counter += length

        return transDict, labels



import pickle
f = open('tl.txt')
tl = pickle.load(f)
td, labs = generalMarkov(tl, lambda x: countLines(x[0]))
data = []
for i in labs:
        data.append(fileParser.normalizeVector(td[i[0]]))
        data2 = []

data = np.array(data)
NaNs = np.isnan(data)
data[NaNs] = 0 #nans to 0


fileParser.corrHeatMap(data, '1st-order Markov of {} files'.format(len(tl)))







