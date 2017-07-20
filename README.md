blackBoxProject
======
**blackboxProject** is the home for work on Kent University's BlueJ [blackbox project](http://www.bluej.org/blackbox.html) at Harvey Mudd college. The code is written in Python 2 and can be used to download, sort, and do preliminary analysis on java source files from Kent's whitebox server.

## Download
**blackboxProject** itself is Python code, so requires no installation except for its dependencies. Simply clone from the github page using, git clone ```$ git clone https://github.com/ndiamant/blackboxProject.git```. Users will need its dependencies: 
* [plyj](https://github.com/musiKk/plyj) 
* matplotlib 
* numpy 
* seaborn 
* pylab 

Use of [t-SNE](https://lvdmaaten.github.io/tsne/) is planned for data visualization, so tsne.py is included for convenience (created by Laurens van der Maaten on 20-12-08, Copyright (c) 2008 Tilburg University. All rights reserved). 

## Overview
**blackboxProject** currently has the following files:
* auction files - directory contains all files made for analysis of errors and coder's tendencies in files containing the Auction() class, a problem made by BlueJ developers 
  * mergeAuctionData.py - merges together the outputs of mySQL search produced by mySQLAuctionQuery.py and the states list produced by ""
  * mySQLAuctionQuery.py - takes in files with names in the format created by the function 'downloadfiles' in fileGrouper.py and makes an SQL query that gets relevant data from mySQL tables on the whitebox server
* payloadReader.py - can read whitebox payload files and write java files using whitebox index files and filter the files. 
* fileParser.py - uses plyj parser to parse java files into abstract syntax trees and then create frequency vectors of syntactic devices for further analysis.
* fileGrouper.py - downloads all javafiles that match user input text (e.g. 'factorial') and groups them by day modified and file ID.
* tsne.py - Created by Laurens van der Maaten on 20-12-08, still working on using it for visualizing blackbox data. 

## Contributors
All work so far on **blackboxProject** has been done by Nathaniel Diamant and Nick Draper from Harvey Mudd College.

### How to contribute

If you want to contribute by adding to the file downloading/organizing infrastrucure or analysis or if you find a bug, e-mail ndiamant@hmc.edu.

## License 
* see [LICENSE](blackboxProject/LICENSE.md) file

## How-to use this code
* see [INSTRUCTIONS](blackboxProject/INSTRUCTIONS.md) file

## Contact
#### Harvey Mudd CS
* Homepage: https://www.cs.hmc.edu/research/
* e-mail: ndiamant@hmc.edu
* Twitter: [@CSTeachingTips](https://twitter.com/csteachingtips "CS Teaching Tips on twitter")

## Funding
This material is based upon work supported by the National Science Foundation under Grant No. 1339404. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
