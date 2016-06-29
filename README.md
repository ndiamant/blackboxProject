# blackboxProject
Home for work on the BlueJ black box project at Harvey Mudd college. Currently has four files:

payloadReader.py - used to read a payload file using an index file

fileParser.py - uses plyj parser to parse java files from readbytes.py

fileGrouper.py - downloads all javafiles that match user input text (e.g. 'factorial') and groups them by day modified and file ID.

tsne.py - Created by Laurens van der Maaten on 20-12-08, still working on using it for visualizing blackbox data. 

Users will need to install [plyj](https://github.com/musiKk/plyj), matplotlib, mpl_toolkits, numpy, seaborn, pylab.
Users should not upload database files.
