import plyj.parser as plyj
try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        import seaborn as sns
except Exception:
        print 'Graphing libraries not imported, do not use graph functions.'
import os 
import time
from matplotlib.mlab import PCA
from os.path import join as pj
import numpy as np
import inspect
import tsne
import random as random
import payloadReader
import subprocess
import shutil
import re

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


def methodInvocationFinder(tree, goal):
        """
        finds a goal method with recursive depth first search
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


def findGoal(tree, goalType, goalName):
        """
        finds a goalType in tree named goalName
        """
        if isinstance(tree, goalType):
                if goalType == str:
                        if goalName in tree:
                                return True, tree
                try:
                        if tree.__dict__['name'] == goalName:
                                return True, tree
                except Exception:
                        pass
        #recursive step if we are at a list
        if isinstance(tree, list):
                for part in tree:
                        result = findGoal(part, goalType, goalName)
                        if result[0]:
                                return result

        #recursive step at a plyj class
        if hasattr(tree,  '__dict__'):
                return findGoal(tree.__dict__.values(), goalType, goalName)

        #leaf case -> can't go any deeper and haven't found goal
        return False, tree


def checkInstance(tree, goalType):
        """
        finds whether or not there is an instance of goalType in the tree
        """
        if isinstance(tree, goalType):
                return True, tree

        #recursive step if we are at a list
        if isinstance(tree, list):
                for part in tree:
                        result = checkInstance(part, goalType)
                        if result[0]:
                                return result

        #recursive step at a plyj class
        if hasattr(tree,  '__dict__'):
                return checkInstance(tree.__dict__.values(), goalType)

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

def loopCounter(tree):
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
        estimates the number of lines in the goal method
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

def delRedundantCols(data):
        """
        removes colums of a repeated value. E.g. [1,1,1]
        """
        return data[:,np.std(data, axis = 0) != 0]

def PCAplot3d(data):
        """
        modified from http://blog.nextgenetics.net/?e=42. 
        Plots the vectors based on the 3 most significant components.
        """
        data = delRedundantCols(data)
        print np.shape(data)
        result = PCA(data)
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
        ax.scatter(pltData[0], pltData[1], pltData[2], '.') # make a scatter plot of blue dots from the data
         
        # make simple, bare axis lines through space:
        xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
        ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # make a red line for the x-axis.
        yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1])), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
        ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r') # make a red line for the y-axis.
        zAxisLine = ((0, 0), (0,0), (min(pltData[2]), max(pltData[2]))) # 2 points make the z-axis line at the data extrema along z-axis
        ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r') # make a red line for the z-axis.
         

        print "variance captured: " + str(result.fracs[0:3])
        # label the axes 
        ax.set_xlabel("principal component 1") 
        ax.set_ylabel("principal component 2")
        ax.set_zlabel("principal component 3")
        ax.set_title("PCA of " + str(len(x)) + " java files")
        plt.show() # show the plot


def PCAplot2d(data):
        """
        plots 2d PCA. Modified from http://blog.nextgenetics.net/?e=42
        """
        data = delRedundantCols(data)
        print np.shape(data)
        result = PCA(data)
        x = []
        y = []
        for item in result.Y:
                x.append(item[0])
                y.append(item[1])

        print "variance captured: " + str(result.fracs[0:2])
        plt.scatter(x, y, marker = '.', c = 'k')
        plt.show()


def freqData(directory, classDict = genClassDict(), recursionIncluded = False):
        """
        prepares the .java files in the specified directory with a narrower freq dict
        and returns data ready for the matplotlib PCA object.
        """
        frequencyList = []
        start = time.time()
        for p, d, f in os.walk(directory): # path, directories, files
                f = sorted(filter(lambda x: ".java" in x, f))
                for i in f:
                        tree = parser.parse_file(pj(p,i))
                        freqVec = treeToFreqDict(tree, classDict).values()
                        if recursionIncluded:
                                freqVec += [int(recursiveMethodFinder(tree)[0])]
                        frequencyList.append(freqVec)
                break # break to avoid walking through all sub directories
        end = time.time()
        print "time elapsed: " + str(end - start)
        data = np.array(frequencyList)
        return data

def plot2dData(data):
        x = []
        y = []
        for point in data:
                x += [point[0]]
                y += [point[1]]
        plt.scatter(x, y, marker='+')
        plt.show()


def plot3dData(data):
        x = []
        y = []
        z = []
        for item in data:
                x.append(item[0])
                y.append(item[1])
                z.append(item[2])

        plt.close('all') # close all latent plotting windows
        fig1 = plt.figure() # Make a plotting figure
        ax = Axes3D(fig1)
        ax.scatter(x, y, z, marker = '.')
        plt.show()

def genCorrelationMatrix(data):
        """
        takes data in row vector form and returns a correlation matrix
        """
        return np.corrcoef(np.transpose(data))


def corrHeatMap(corrmat, title = '', labels = []):
        """draws a correllation heat map using SNS corrmat"""
        f, ax = plt.subplots(figsize=(12, 9))
        ticks = int(round(corrmat.shape[0]/10,-1))
        if labels:
                sns.heatmap(corrmat, vmax = .9, square = True, xticklabels = labels, yticklabels = labels)
        elif ticks > 5:
                sns.heatmap(corrmat, vmax = .9, square = True, xticklabels = ticks, yticklabels = ticks)
        else:
                sns.heatmap(corrmat, vmax = .9, square = True)
        if title:
                sns.plt.title(title)
        #f.tight_layout()
        plt.show()


def normalizeVector(vector):
        """
        l2 normalization of vector
        """
        return vector / np.linalg.norm(vector)

def normalizeRows(arr):
        """
        l2 normalization of rows of arr (numpy array).
        """
        return np.apply_along_axis(normalizeVector, 1, arr)

#dangerous AF!!!!!
def getErrMessages(textList, tempDirName = 'temp', className = 'temp.java'):
        """
        gets error messages in the same order as the textList 
        by attempting to compile the code
        """
        os.mkdir(tempDirName)       
        os.chdir(tempDirName)
        payloadReader.writeFiles(textList, os.getcwd())
        print os.getcwd()
        errors = []
        for p, d, f in os.walk('.'): # path, directories, files
                for i in f:
                        if className:
                                os.rename(i, className)
                        error = subprocess.Popen(['javac', className], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        error = error.communicate()[1]
                        errors.append(error)
                break
        os.chdir('..')
        print os.getcwd()
        shutil.rmtree(tempDirName)
        return errors


def parseError(error):
        """
        takes a java compiler error as formatted by javac and 
        returns a tuple of (error line, error text)
        """
        if not error:
                return None
        errTuple = re.search('(.*).java:(.*): error: (.*)', error).groups()
        return int(errTuple[1]), errTuple[2]


def parseErrors(errList):
        """
        takes a list of errors in the format of the output of getErrMessages and 
        returns a list of tuples of (error line, error text)
        """
        return map(parseError, errList)


def getMethodLines(methodName, text):
        """
        returns the start and end line of the 
        target method in a tuple, (startLine, endLine)
        """
        lineNums = list(enumerate(text.split('\n')))
        startLine = filter(lambda t: 'printDetails' in t[1], lineNums)[0][0]
        parenCount = 1
        for line in lineNums[startLine + 1::]:
                parenCount += line[1].count('{')
                parenCount -= line[1].count('}')
                if parenCount == 0:
                        return startLine, line[0]
        return startLine, lineNums[-1][0]