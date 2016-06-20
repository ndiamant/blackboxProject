import plyj.parser as plyj
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os 
import time
from matplotlib.mlab import PCA
from os.path import join as pj
import numpy as np
import inspect

parser = plyj.Parser()

# all finder methods return a boolean if the target is found followed
# by the tree of the target

# a tuple of all of the classes in plyj
plyj_classes = tuple(x[1] for x in inspect.getmembers(plyj,inspect.isclass))


def genClassDict():
    """
    returns a dictionary with keys of all the classes in plyj with values of zero
    """
    plyj_dict = {}

    for plyj_class in plyj_classes:
        plyj_dict[plyj_class] = 0

    return plyj_dict
 

def methodFinder(tree, goal):
    """
    finds a goal method with recursive depth first search
    """
    
    #base case if we have arrived at our goal method
    if isinstance(tree, plyj.MethodDeclaration):
            if tree.__dict__['name'] == goal:
                return True, tree

    #recursive step if we are at a list
    if isinstance(tree, list):
        for part in tree:
            result = methodFinder(part, goal)
            if result[0]:
                return result

    #recursive step at a plyj class
    if hasattr(tree,  '__dict__'):
        return methodFinder(tree.__dict__.values(), goal)

    #leaf case -> can't go any deeper and haven't found goal
    return False, tree





def recursiveMethodFinder(tree):
    """
    finds if there is a recursive method
    """
    #base case where we find a method 
    if isinstance(tree, plyj.MethodDeclaration):
            #check if the method invokes itself 
            if methodInvocationFinder(tree, tree.__dict__['name'])[0]:
                return True, tree

    #recursive step if we are at a list
    if isinstance(tree, list):
        for part in tree:
            result = recursiveMethodFinder(part)
            if result[0]:
                return result

    #recursive step at a plyj class
    if hasattr(tree,  '__dict__'):
        return recursiveMethodFinder(tree.__dict__.values())

    #leaf case -> can't go any deeper and haven't found goal
    return False, tree



def methodInvocationFinder(tree, goal):
    """
    finds a goal method invocation with recursive depth first search
    """
    
    #base case if we have arrived at our goal method
    if isinstance(tree, plyj.MethodInvocation):
            if tree.__dict__['name'] == goal:
                return True, tree

    #recursive step if we are at a list
    if isinstance(tree, list):
        for part in tree:
            result = methodInvocationFinder(part, goal)
            if result[0]:
                return result

    #recursive step at a plyj class
    if hasattr(tree,  '__dict__'):
        return methodInvocationFinder(tree.__dict__.values(), goal)

    #leaf case -> can't go any deeper and haven't found goal
    return False, tree


def loopDepthFinder(tree, goal):
    """
    finds the loop depth of a method
    """
    methodTree = methodFinder(tree, goal)

    if not methodTree[0]:
        print 'method does not exist'
        return

    tree = methodTree[1]

    return forLoopCounter(tree)

def forLoopCounter(tree):
    """
    recursively counts number of loops in tree
    """
    forResult = classFinder(tree, plyj.For)
    whileResult = classFinder(tree, plyj.While)
    if forResult[0]:
        return 1 + forLoopCounter(forResult[1].__dict__.values())

    if whileResult[0]:
        return 1 + forLoopCounter(whileResult[1].__dict__.values())

    return 0



    
def classFinder(tree, goal):
    """
    finds a target class
    """
    if isinstance(tree, goal):
            return True, tree
    
    if isinstance(tree, list):
        for part in tree:
            result = classFinder(part, goal)
            if result[0]:
                return result

    if hasattr(tree,  '__dict__'):
        return classFinder(tree.__dict__.values(), goal)

    return False, tree



def lineCounter(tree, goal):
    """
    finds the number of lines in the goal method
    """
    methodTree = methodFinder(tree, goal)
    if not methodTree[0]:
        print "no such method"
        return

    return lineCounterHelper(methodTree[1])



def lineCounterHelper(methodTree):
    """
    helper to lineCounter finds the number of lines from a
    method's tree
    """
    total = 0
    if isinstance(methodTree, plyj_classes):
        total += 1

    if isinstance(methodTree, list):
        for part in methodTree:
            total += lineCounterHelper(part)

    if hasattr(methodTree, '__dict__'):
        total +=  lineCounterHelper(methodTree.__dict__.values())

    return total




def treeToFreqDict(tree, classDict = genClassDict()):
    """
    creates a multinomial frequency dictionary of the class types that 
    appear in a tree
    """
    plyj_dict = classDict.copy()
    def addToDict(tree):
        if type(tree) in plyj_dict:
            plyj_dict[type(tree)] = plyj_dict[type(tree)] + 1

        if isinstance(tree, list):
            for branch in tree:
                addToDict(branch)

        if hasattr(tree,  '__dict__'):
            addToDict(tree.__dict__.values())

    addToDict(tree)
    return plyj_dict

def cosSimilarity(freqDict1, freqDict2):
    """
    finds cosine similarity between 2 plyj class frequency dictionaries
    by treating them as vectors.
    """
    magnitude1 = 0
    magnitude2 = 0
    dotProduct = 0
    for key in freqDict1:
        dotProduct += freqDict1[key] * freqDict2[key]
        magnitude1  += freqDict1[key]**2
        magnitude2  += freqDict2[key]**2

    return dotProduct / (magnitude1**.5 * magnitude2**.5)

def countRecursiveMethods(directory):
    numRecursiveMethods = 0
    start = time.time()
    for p, d, f in os.walk(directory): # path, directories, files
        f = filter(lambda x: ".java" in x, f)
        for i in f:
            tree = parser.parse_file(pj(p,i))
            if recursiveMethodFinder(tree)[0]:
                numRecursiveMethods += 1


        break # break to avoid walking through all sub directories
    end = time.time()
    print "time elapsed:" + str(end - start)
    return numRecursiveMethods


def freqPCA(directory):
    """
    runs PCA on the .java files in the specified directory
    and returns the matplotlib PCA object.
    """
    frequencyList = []
    start = time.time()
    for p, d, f in os.walk(directory): # path, directories, files
        f = filter(lambda x: ".java" in x, f)
        for i in f:
            frequencyList.append(treeToFreqDict(parser.parse_file(pj(p,i))).values())
        break # break to avoid walking through all sub directories
    end = time.time()
    print "time elapsed:" + str(end - start)
    data = np.array(frequencyList)
    data = data[:,np.std(data, axis = 0) != 0] #removes columns with all repeated values 
    print np.shape(data)
    return PCA(data)

def PCAplot3d(PCAresult):
    """
    modified from http://blog.nextgenetics.net/?e=42. 
    Plots the vectors based on the 3 most significant components.
    """
    result = PCAresult
    x = []
    y = []
    z = []
    for item in result.Y:
        x.append(item[0])
        y.append(item[1])
        z.append(item[2])

    plt.close('all') # close all latent plotting windows
    fig1 = plt.figure() # Make a plotting figure
    ax = Axes3D(fig1) # use the plotting figure to create a Axis3D object.
    pltData = [x,y,z] 
    ax.scatter(pltData[0], pltData[1], pltData[2], 'asdfasf') # make a scatter plot of blue dots from the data
     
    # make simple, bare axis lines through space:
    xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # make a red line for the x-axis.
    yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1])), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r') # make a red line for the y-axis.
    zAxisLine = ((0, 0), (0,0), (min(pltData[2]), max(pltData[2]))) # 2 points make the z-axis line at the data extrema along z-axis
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r') # make a red line for the z-axis.
     

    print result.fracs[0:3]
    # label the axes 
    ax.set_xlabel("principal component 1") 
    ax.set_ylabel("principal component 2")
    ax.set_zlabel("principal component 3")
    ax.set_title("PCA of 100 java files")
    plt.show() # show the plot


def PCAplot2d(PCAresult):
    """
    plots 2d PCA. Modified from http://blog.nextgenetics.net/?e=42
    """
    result = PCAresult
    x = []
    y = []
    for item in result.Y:
        x.append(item[0])
        y.append(item[1])

    print result.fracs[0:2]
    plt.scatter(x, y)
    plt.show()


def narrowPCA(directory):
    """
    PCA with only for loop, while loop, recursion presence, methood declaration,
    variable declaration, Variable, And, Or, ArrayCreation
    """
    narrowClassDict = {plyj.For:0, plyj.While:0, plyj.MethodDeclaration:0, plyj.ArrayCreation:0,
                        plyj.VariableDeclaration:0}
    #narrowClassDict = {plyj.VariableDeclaration:0, plyj.MethodDeclaration:0}
    frequencyList = []
    start = time.time()
    for p, d, f in os.walk(directory): # path, directories, files
        f = filter(lambda x: ".java" in x, f)
        for i in f:
            tree = parser.parse_file(pj(p,i))
            frequencyList.append(treeToFreqDict(tree, narrowClassDict).values()  + [int(recursiveMethodFinder(tree)[0])])
        break # break to avoid walking through all sub directories
    end = time.time()
    print "time elapsed:" + str(end - start)
    data = np.array(frequencyList)
    data = data[:,np.std(data, axis = 0) != 0] #removes columns with all repeated values 
    #return data
    return PCA(data) 

def plot2dData(data):
    x = []
    y = []
    for point in data:
        x += [point[0]]
        y += [point[1]]
    plt.scatter(x, y)
    plt.show()


result = narrowPCA('/Users/cssummer16/Documents/summerResearch/blackboxProject/javafiles')
PCAplot2d(result)
PCAplot3d(result)


# narrow by problem


