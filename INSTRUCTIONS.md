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

Structure
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
_createIndexList(indexFile, directory = os.getcwd())_ takes the string name of an index file and the directory it's in (string). It returns a list of tuples with (source file id, master event id, file start position, file length, compilation success [1 or 0]). This can be used by the [readFiles](#readfiles) function to make a list of text files. 

##### Todo
* complete for now

======
#### readFiles
_readFiles(payloadFile, indexList, directory = os.getcwd())_ takes an index list made by [_createIndexList_](#createindexlist), the string name of a payload file, and the directory (string) the payload is in. It returns a list of strings where each string is an entire java file from the payload. The text can be put into individual files using [_writeFiles_](#writefiles).

##### Todo
* Considering making [_readFiles_](#readfiles) return a list of tuples with (text, index) so that the index can still be used for stuff like naming the files that get written from the text list.

======
#### writeFiles

_writeFiles(textList, directory = os.getcwd(), name = "payloadFile")_ takes a text list made by [_readFiles_](#readfiles) and a directory (string) to write files with the .java extension, and a name to call the java files. The files are named "[name][number].java", where number is an iterated integer counting from zero.

##### Todo
* If [_readFiles_](#readfiles) is changed as suggested in its Todo, then [_writeFiles_](#writefiles) will have to be changed accordingly. If this change is implemented, I will also change the naming convention to use the index.

======
#### writeByFileID

 _writeByFileID(indexList, payloadFileName, writeDir, readDir = os.getcwd(), willFilter = False, filterText = '')_ takes an index list from [_createIndexList_](#createindexlist), strings of the payload file's name, the directory files will be written into, the directory files the payload is in, and whether the files will be filtered to contain filterText. It creates directories with file IDs from the index list and writes files from the payload file into those directory. This makes a directory of directories named afer file names that contain all of the files of one file ID from the payload. 

##### Todo
* Add name argument like [_writeFiles_](#writefiles) has and maybe more filtering options. 
* If [_readFiles_](#readfiles) is modified as suggested in its Todo, then [_writeByFileID_](#writebyfileid) could be broken into two parts allowing for more modularity.

======
#### Filters

There are two simple filter functions. _filterByCompilability(indexList)_ takes an index list from [_createIndexList_](#createindexlist) and returns an index list of indices corresponding to compilable java files. _filterByText(textList, filterText)_ filters a text list made by [_readFiles_](#readfiles) leaving only text that contains filterText. _filterForAscii(textList)_ filters a text list and returns a list of text with pure ascii characters.

##### Todo
* If [_readFiles_](#readfiles) changes its text list format, the two functions that filter text lists will have to be modified accordingly.

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
_getTextFiles(indexDirectory, targetDirectory, targetText, userName)_ takes the string names of a directory containing as many whitebox index files as you want, a directory to write java files into, text to filter for, and your whitebox user name. _getTextFiles_ uses scp and then deletes the payload files one at a time to reduce memory needs. If you have not set up an ssh key, it will prompt you for your password. It creates directories organized by day and then file ID as follows:
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
* * add way to interact with external hard drive to avoid pesky download times

======
#### groupByFileID
_groupByFileID(payloadDirectory, targetDirectory)_ takes the string name of a directory made by [[_getTextFiles_](#gettextfiles), and the string name of a new directory to copy files into. It removes the date directories, and organizes only by file ID. In each directory individual files change in ascending number order. This function is especially useful for examining how individual files change over time. The target directory's structure: 
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
* Replace '/*/*' with something that works on both windows and unix and DOS.

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

