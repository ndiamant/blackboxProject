# blackboxProject Instructions #
------
These instructions are meant to explain how to use the **blackboxProject** without going into detail about how everything works. If you're looking to understand how something works or think you could make it work better, e-mail me, ndiamant@hmc.edu! I'm open to explaining and suggestions.

##Beginning##
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

## Structure
------
The most fundamental of the programs is payloadReader.py. In general, _payloadReader.py_ is used to take an index file from whitebox (like "index-2016-01-08") and a corresponding payload file ("payload-2016-01-08") and separate the java files contained in the payload. To get individual index and payload files, you can scp from the whitebox server: ```$ scp USER@white.kent.ac.uk:/data/compile-inputs/payload-2016-01-08 ~/target/directory```. ([_fileGrouper.py_](#filegrouper.py) will do it for you). 

### payloadReader.py
Most of the code in _payloadReader.py_ is helper functions. Here are some that a user might want. 

#### Index
* [_createIndexList_](#createindexlist)
* [_readFiles_](#readfiles)
* [_writeFiles_](#writefiles)
* [_writeByFileID_](#writebyfileid)
* [_Filters_](#filters)

#### createIndexList
======
_createIndexList(indexFile, directory = os.getcwd())_ takes the string name of an index file and the directory it's in (string). It returns a list of tuples with (source file id, master event id, file start position, file length, compilation success [1 or 0]). This can be used by the [readFiles](#readfiles) function to make a list of text files. 

##### Todo
complete for now

#### readFiles
======
_readFiles(payloadFile, indexList, directory = os.getcwd())_ takes an index list made by [_createIndexList_](#createindexlist), the string name of a payload file, and the directory (string) the payload is in. It returns a list of strings where each string is an entire java file from the payload. The text can be put into individual files using [_writeFiles_](#writefiles).

##### Todo
Considering making [_readFiles_](#readfiles) return a list of tuples with (text, index) so that the index can still be used for stuff like naming the files that get written from the text list.

#### writeFiles
======
_writeFiles(textList, directory = os.getcwd(), name = "payloadFile")_ takes a text list made by [_readFiles_](#readfiles) and a directory (string) to write files with the .java extension, and a name to call the java files. The files are named "[name][number].java", where number is an iterated integer counting from zero.

##### Todo
If [_readFiles_](#readfiles) is changed as suggested in its Todo, then [_writeFiles_](#writefiles) will have to be changed accordingly. If this change is implemented, I will also change the naming convention to use the index.

#### writeByFileID
======
 _writeByFileID(indexList, payloadFileName, writeDir, readDir = os.getcwd(), willFilter = False, filterText = '')_ takes an index list from [_createIndexList_](#createindexlist), strings of the payload file's name, the directory files will be written into, the directory files the payload is in, and whether the files will be filtered to contain filterText. It creates directories with file IDs from the index list and writes files from the payload file into those directory. This makes a directory of directories named afer file names that contain all of the files of one file ID from the payload. 

##### Todo
Add name argument like [_writeFiles_](#writefiles) has and maybe more filtering options. If [_readFiles_](#readfiles) is modified as suggested in its Todo, then [_writeByFileID_](#writebyfileid) could be broken into two parts allowing for more modularity.

#### Filters
======
There are two simple filter functions. _filterByCompilability(indexList)_ takes an index list from [_createIndexList_](#createindexlist) and returns an index list of indices corresponding to compileable java files. _filterByText(textList, filterText)_ filters a text list made by [_readFiles_](#readfiles) leaving only text that contains filterText. _filterForAscii(textList)_ filters a text list and returns a list of text with pure ascii characters.

##### Todo
If [_readFiles_](#readfiles) changes its text list format, the two functions that filter text lists will have to be modified accordingly.

### fileGrouper.py

