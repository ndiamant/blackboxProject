### IGNORE THIS FILE FOR NOW ###


from collections import defaultdict
import numpy as np
import fileParser

def countLines(text):
        return text.count('n')


def transitionFreq(textList):
        """
        returns a dictionary keyed with a line count with a value of
        a np array with the number of transitions to all of the other states
        labelled by labels
        """
        lengths = map(lambda entry: countLines(entry[0]), textList)
        labels = range(0, max(lengths) + 1)
        transDict = defaultdict(lambda: np.array([0] * (max(lengths) + 1)))
        for index in xrange(1, len(textList) - 1):               
                # transDict[lengths[index]]
                # prev = lengths[index - 1]
                # current = lengths[index]
                following = lengths[index + 1]
                # transDict[lengths[index]][prev] += 1
                #transDict[lengths[index]][current] += 1
                
                # if following > len(transDict[lengths[index]]) - 1:
                #         print len(transDict[lengths[index]]), following

                transDict[lengths[index]][following] += 1
        return transDict, labels


import pickle
f = open('tl.txt')
tl = pickle.load(f)
td, labs = transitionFreq(tl)
print td.values()[0]
data = []
for i in labs:
        data.append(fileParser.normalizeVector(td[i]))

data = np.array(data)
NaNs = np.isnan(data)
data[NaNs] = 0 #nans to 0

print data[0]

fileParser.corrHeatMap(data, None)