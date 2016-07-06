blackboxProject Instructions 
======
These instructions are meant to explain how to use the **blackboxProject** without going into detail about how everything works. If you're looking to understand how something works or think you could make it work better, e-mail me, ndiamant@hmc.edu! I'm open to explaining and suggestions.

Beginning
------
Begin by cloning the repository, ```$ git clone https://github.com/ndiamant/blackboxProject.git```. Next, 
make sure to install all of the dependencies. 
* [plyj](https://github.com/musiKk/plyj) 
* matplotlib 
* mpl_toolkits 
* numpy 
* seaborn 
* pylab 
Plyj has a setup.py file, so can be installed by running ```$ python setup.py install```. 
The rest can be installed with ```$ pip install matplotlib numpy seaborn pylab```. 
Plyj only works in Python 2.

### Glossary
* [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree): a tree data structure that represents code's structure. Generated from code to give to the compiler.
* blackbox: the read only server that collects all of the java files from blueJ
* file ID: part of the index, is a persistent identifier for a file used to track a file over multiple edits
* index: A tuple of integers taken from the byte code in an index file from whitebox: (source file id, master event id, file start position, file length, compilation success [1 or 0])
* index file: a file from white box filled with byte codes representing (source file id, master event id, file start position, file length, compilation success [1 or 0]) for the files in a payload file
* indexList: A list of index tuples
* payload file: a text file from whitebox full of unseparated java source files written by BlueJ users. Can be indexed into using an index file
* [plyj](https://github.com/musiKk/plyj): an external python library used to create abstract syntax trees from java files
* whitebox: the server members of the blackbox project interact with and download payload and index files from.
* text list: a list of (string, index) tuples where each string is all of the text of one source file from a payload file

blackboxProject Structure
------
The most fundamental of the programs is payloadReader.py. In general, _payloadReader.py_ is used to take an index file from whitebox (like "index-2016-01-08") and a corresponding payload file ("payload-2016-01-08") and separate the java files contained in the payload. To get individual index and payload files, you can scp from the whitebox server: ```$ scp user@white.kent.ac.uk:/data/compile-inputs/payload-2016-01-08 ~/target/directory```. ([_fileGrouper.py_](#filegrouperpy) will do it for you). 

------
### payloadReader.py
Most of the code in _payloadReader.py_ is helper functions. Here are some that a user might want. 

#### Index
* [_createIndexList_](#createindexlist)
* [_readFiles_](#readfiles)
* [_writeFiles_](#writefiles)
* [_writeByFileID_](#writebyfileid)
* [_Filters_](#filters)

======
#### createIndexList
_createIndexList(indexFile, directory = os.getcwd())_ takes
* indexFile: the string name of an index file
* directory: the directory it's in (string). 

Returns: a list of tuples with (source file id, master event id, file start position, file length, compilation success [1 or 0]). This can be used by the [readFiles](#readfiles) function to make a list of text files. 

##### Todo
* complete for now

======
#### readFiles
_readFiles(payloadFile, indexList, directory = os.getcwd())_ takes 
* payloadFile: the string name of a payload file
* indexList: an index list made by [_createIndexList_](#createindexlist)
* directory: the directory (string) the payload is in. 

Returns: a list of (string, index) tuples where each string is all of the text of one source file from a payload file. The text can be put into individual files using [_writeFiles_](#writefiles).

##### Todo
* ~~Considering making [_readFiles_](#readfiles) return a list of tuples with (text, index) so that the index can still be used for stuff like naming the files that get written from the text list.~~

======
#### writeFiles

_writeFiles(textList, directory = os.getcwd(), nameNum = 0)_ takes
* textList: a text list made by [_readFiles_](#readfiles)
* directory: a directory (string) where it will write files with the .java extension
* nameNum: where the name iterator starts from.
 
Creates: a directory filled with .java files with the following structure.
Returns: where nameNum left off so that it can be used as an argument if you want to use writeFiles again in the same directory.
```
2015-12-11
├── payload0.java
├── payload1.java
├── payload2.java
└── payload3.java
```

##### Todo
* ~~If [_readFiles_](#readfiles) is changed as suggested in its Todo, then [_writeFiles_](#writefiles) will have to be changed accordingly. If this change is implemented, I will also change the naming convention to use the index.~~

======
#### writeByFileID

 _writeByFileID(indexList, payloadFileName, writeDir, readDir = os.getcwd(), willFilter = False, filterText = '')_ takes 
 * indexList: an index list from [_createIndexList_](#createindexlist)
 * payloadFileName: string of the payload file's name
 * writeDir: string of the directory where files will be written into
 * readDir: string  of the directory where the payload is
 * willFilter: boolean of whether the files will be filtered to contain filterText.
 * filterText: string to filter for text containing it. 
 
 Creates: directories with file IDs from the index list and writes files from the payload file into those directory. This makes a directory of directories named afer file names that contain all of the files of one file ID from the payload. 

##### Todo
* Add name argument like [_writeFiles_](#writefiles) has and maybe more filtering options. 
* If [_readFiles_](#readfiles) is modified as suggested in its Todo, then [_writeByFileID_](#writebyfileid) could be broken into two parts allowing for more modularity.
* Really slow for some reason. Maybe calls _writeFiles_ too much? Make faster

======
#### Filters

There are two filter functions. 
_filterByCompilability(indexList)_ takes
* indexList: an index list from [_createIndexList_](#createindexlist) 

Returns: an index list of indices corresponding to compilable java files. 
_filterByText(textList, filterText)_ takes
* textList: a text list made by [_readFiles_](#readfiles)
* filterText: string that all remaining strings in textList will contain

Returns: a text list of only strings that contains filterText. 

_filterForAscii(textList)_ takes
* textList: a text list made by [_readFiles_](#readfiles)

Returns: a list of text with pure ascii characters.

##### Todo
* If [_readFiles_](#readfiles) changes its text list format, the functions that filter text lists will have to be modified accordingly.

=====
#### Examples

Let's say we have an index file named "index-2016-01-08" and a payload file named "payload-2016-01-08" in the same directory as [_payloadReader.py](#payloadreaderpy) and we want to fill a directory called "javafiles" with all of the compiliable java files in payload that contain the text "factorial", and we want the java files to be named "test[iterator].java".

```$ python -i payloadReader.py```
```python
fname = "index-2016-01-08"
indList = filterByCompilability(createIndexList(fname)) #create the index list filtered for compilability
textList = readFiles("payload-2016-01-08", indList) #create the text list
textList = filterByText(textList, 'factorial') #filter so all text contains "factorial"
writeFiles(textList, os.getcwd() + "/javafiles", 'test') #write the files into the /javafiles directory
#If instead we want to group the files by their file IDs and find files that contain "fibonacci"
writeByFileID(indList, "payload-2016-01-08", os.getcwd() + "/javafiles", os.getcwd(), True, 'fibonacci')
```

------
### fileGrouper.py
_fileGrouper.py_ uses [_payloadReader.py_](#payloadreaderpy) to download and organize java files from whitebox in two different ways.

#### Index
* [_getTextFiles_](#getextfiles)
* [_groupByFileID_](#groupbyfileid)

======
#### getTextFiles
_getTextFiles(indexDirectory, targetDirectory, targetText, userName)_ takes 
* indexDirectory: the string name of a directory containing as many whitebox index files as you want
* targetDirectory: the string name of a  directory to write java files into
* targetText: text to filter for
* userName: your whitebox user name. 

Note: _getTextFiles_ uses scp and then deletes the payload files one at a time to reduce memory needs. If you have not set up an ssh key, it will prompt you for your password.

Creates: directories organized by day and then file ID as follows:

```
./javafiles/
├── 2015-12-11
│   ├── 23486260
│   │   ├── payloadFile0.java
│   │   ├── payloadFile1.java
│   │   └── payloadFile2.java
│   ├── 26796734
│   │   ├── payloadFile0.java
│   │   └── payloadFile1.java
│   └── 26875865
│       ├── payloadFile0.java
└── 2016-06-17
    ├── 34640886
    │   └──  payloadFile0.java
    ├── 34651751
    │   ├── payloadFile0.java
    │   └── payloadFile5.java
    └── 34651753
        └── payloadFile0.java
```
##### Todo
* If [_readFiles_](#readfiles) is changed as suggested in its Todo, then [_getTextFiles_](#gettextfiles) will have to be adjusted accordingly.
* Make faster!
* add way to interact with external hard drive to avoid pesky download times

======
#### groupByFileID
_groupByFileID(payloadDirectory, targetDirectory)_ takes 
* payloadDirectory: the string name of a directory made by [[_getTextFiles_](#gettextfiles)
* targetDirectory: the string name of a new directory to copy files into. 

Creates: removes the date directories from the structure of the directory made by [_getTextFiles_](#gettextfiles), and organizes only by file ID. In each directory individual files change in ascending number order. This function is especially useful for examining how individual files change over time. The target directory's structure: 
```
./fileIDs/
├── 11906466
│   ├── payload1670.java
│   ├── payload1671.java
│   └── payload1672.java
├── 17425200
│   └── payload6447.java
├── 21393086
│   └── payload542.java
└── 34804768
    ├── payload7111.java
    ├── payload7112.java
    └── payload7149.java
```
##### Todo
* Replace '/\*/\*' with something that works on both windows and unix and DOS.

=====
#### Examples

Let's say we want to download all of the java file that contain "fibonacci" into a directory called "javafiles" and then sort them by only file ID into another directory called fileIDs. 
```$ scp user@white.kent.ac.uk:/data/compile-inputs/index* ~/Desktop/indices/ #download all index files to desktop```
```python
#download payloads, convert to java files, and organize into javafiles directory
getTextFiles('/Users/username/Desktop/indices', os.getcwd() + '/javaFiles', 'fibonacci’,  ‘user’) 
#copy files into new structure in fileIDs directory.
groupByFileID(os.getcwd() + '/javaFiles', os.getcwd() + '/fileIDs') 
```

------
### fileParser.py
_fileParser.py_ uses java files prepared by [_payloadReader.py_](#payloadreaderpy) and [_fileGrouper.py_](#filegrouperpy) to run various analyses. [Plyj](https://github.com/musiKk/plyj) parses java files into abstract sytax trees, which we can search for structure and syntactic devices. The following are some useful methods.

#### Index
* [recursive tree searches](#recursive-tree-searches)
* [_genClassDict_](#genclassdict)
* [_treeToFreqDict_](#treetofreqdict)
* [_cosSimilarity_](#cossimilarity)
* [_freqData_](#freqdata)
* [PCA functions](#pca-functions)
* [correllation functions](#correlation-functions)

======
#### recursive tree searches

All of the tree search functions use recursive depth first search on an abstract sytax tree generated by [plyj](https://github.com/musiKk/plyj). They all take an abstract syntax tree generated by plyj. You can do thus with 
```python
tree = parser.parse_file(path)
```
Some also take a goal to search for. Here is a brief summary of the current tree search functions.

| Method name | arguments | returns | return meaning |
|-------------|-----------|---------|----------------|
| _recursiveMethodFinder(tree)_ | plyj tree |(boolean, tree)| (recursion present?, subtree of recursive method) |
| _loopCounter(tree)_ | plyj tree | integer |number of loops in the tree |
| _methodFinder(tree, goal)_ | plyj tree, method name | (boolean, tree) | (method found?, subtree of found method) |
| _classFinder(tree)_ | plyj tree, goal class | (boolean, tree) |(class found?, subtree of found class) |
| _loopDepthFinder(tree)_ | plyj tree of a method| integer | depth of loops found in method|

#### Todo
* Comment code better
* methodFinder and classFinder could be generalized into an object finder function
* are these useful?

======
#### genClassDict

_genClassDict()_ takes no arguments. 

Returns: dictionary with plyj syntactic devices as keys and 0 (integer) as values. 
E.g. 
```python
({<class 'plyj.model.While'>: 0, <class 'plyj.model.ArrayAccess'>: 0, ..., 'plyj.model.ClassDeclaration'>: 0}
```
#### Todo
* Complete for now

======
#### treeToFreqDict

_treeToFreqDict(tree, classDict = genClassDict())_ takes
* tree: a plyj tree to make a frequency dictionary from
* classDict: a dictionary of plyj classes, which represent syntactic devices, to use as keys in the frequency dictionary
 
Returns: a dictionary with plyj classes as keys and the frequency of those class occurences in the plyj tree as the values. E.g. 
```python
({<class 'plyj.model.While'>: 5, <class 'plyj.model.ArrayAccess'>: 0, ..., 'plyj.model.ClassDeclaration'>: 1}
```
To convert to a vector, use ```dict.values()```.
#### Todo
* Complete for now

======
#### cosSimilarity

_cosSimilarity(freqDict1, freqDict2)_ takes
* freqDict1: the first frequency dictionary produced by [_treeToFreqDict_](#treetofreqdict)
* freqDict2: the second frequency dictionary produced by [_treeToFreqDict_](#treetofreqdict)

Returns: Simple [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) as if the dictionaries were vectors.

#### Todo
* Add normalization option

======
#### freqData

_freqData(directory, classDict = genClassDict(), recursionIncluded = False)_ takes
* directory: the string name of a directory filled with .java files
* classDict: a dictionary with plyj classes as keys and zeroes as values, like what is produced [_genClassDict_](#genclassdict).
* recursionIncluded: a boolean whether or not to include the presence of recursion (0 or 1) as the last column of the resultant array. 

Return: a numpy array where columns are frequencies of the syntactic devices included in classDict and each row is a java file.

#### Todo
* complete for now

======
#### PCA functions

The PCA (principle component analysis) functions use [matplotlib's PCA](#http://matplotlib.org/api/mlab_api.html#matplotlib.mlab.PCA) function to plot frequency data generated by [_freqData_](#freqdata) in visualizeable dimensions. The basic idea of PCA is to capture the highest variance affine lines in the data and represent the data as linear combinations of those. The hope is to find some structure in the data.

_PCAplot2d(data)_ takes
* data: frequency array from [_freqData_](#freqdata)

Plots: 2d graph of resultant PCA.   

_PCAplot3d(data)_ takes
* data: frequency array from [_freqData_](#freqdata)

Plots: 3d graph of resultant PCA. Code modified from ttp://blog.nextgenetics.net/?e=42.  

#### Todo
* Investigate clustering
* Investigate t-SNE as alternative

======
#### correlation functions

These functions are used to find correllations between the frequencies of different syntactic devices and structures (e.g. while loops vs. recursion).

_genCorrelationMatrix(data)_ takes
* data: frequency array from [freqData](#freqdata)

Returns: a correlation matrix made by numpy. Entry i,j is the matrix is the correlation between the ith and jth variables in the frequency vector.

_corrHeatMap(corrmat, variableDict)_ takes
* corrMat: a correlation matrix that can be generated with _genCorrelationMatrix_.
* variableDict: planned feature to label produced graphic. To produce a key, the user can use 
```python
for label in enumerate(variableDict)
 print label
```
Plots: a heat map of the correllation matrix.
#### Todo
* Add more structural options / more flexibility for the user to add them
* Add mutual pairwise information

=====
#### Examples

Let's say we have a java file called "test.java" in the directory "/javafiles" and we want to see if it has a recursive method. 
```$ python -i fileParser.py```
```python
tree = parser.parse('/javafiles/test.java') #tree is a plyj abstract syntax file
print recursiveMethodFinder(tree)[0] #get the boolean of whether recursion is present from the tuple (boolean, tree)
```
What if we want to create a 3d PCA plot and a correlation matrix with all of plyj's syntactic devices and recursion as the the columns from the java files contained in /javafiles. 
```$ python -i fileParser.py```
```python
data = freqData('javafiles', True) #generate the frequency data
PCAplot3d(data) #run PCA and plot the data in 3d
data = normalizeRows(data) #l2 normalize the rows of data
cm = genCorrelationMatrix(data) #generate the correlation matrix
corrHeatMap(cm, None) #plot a heat map of the correlation matrix
```
This should produce something like the following graphics.
![PCA 3d](https://github.com/ndiamant/blackboxProject/blob/master/figure_1.png)
![heat map](https://github.com/ndiamant/blackboxProject/blob/master/figure_2.png)


Big Todos
-------
* replace all path additions with os.join
* improve commenting
