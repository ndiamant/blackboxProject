import plyj.parser as plyj
import os 
from os.path import join as pj

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




def treeToFreqDict(tree):
    """
    creates a multinomial frequency dictionary of the class types that 
    appear in a tree
    """
    plyj_dict = genClassDict()

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

numRecursiveMethods = 0

for p, d, f in os.walk('javafiles'): # path, directories, files
    f = filter(lambda x: ".java" in x, f)
    for i in f:
        tree = parser.parse_file(pj(p,i))
        print i
        if recursiveMethodFinder(tree)[0]:
            numRecursiveMethods += 1


    break # break to avoid walking through all sub directories

print numRecursiveMethods


