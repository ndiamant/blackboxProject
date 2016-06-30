blackBoxProject
======
**blackboxProject** is the home for work on Kent University's BlueJ [blackbox project](http://www.bluej.org/blackbox.html) at Harvey Mudd college. The code is written in Python 2 and can be used to download, sort, and do preliminary analysis on java source files from Kent's whitebox server.

## Download
**blackboxProject** itself is Python code, so requires no installation except for its dependencies. Simply clone from the github page using, git clone ```$ git clone https://github.com/ndiamant/blackboxProject.git```. Users will need its dependencies: 
* [plyj](https://github.com/musiKk/plyj) 
* matplotlib 
* mpl_toolkits 
* numpy, seaborn 
* pylab 

Use of [t-SNE](https://lvdmaaten.github.io/tsne/) is planned for data visualization, so tsne.py is included for convenience (created by Laurens van der Maaten on 20-12-08, Copyright (c) 2008 Tilburg University. All rights reserved). 

## Overview
**blackboxProject** currently has four files:
* payloadReader.py - can read whitebox payload files and write java files using whitebox index files and filter the files. 
* fileParser.py - uses plyj parser to parse java files into abstract syntax trees and then create frequency vectors of syntactic devices for further analysis.
* fileGrouper.py - downloads all javafiles that match user input text (e.g. 'factorial') and groups them by day modified and file ID.
* tsne.py - Created by Laurens van der Maaten on 20-12-08, still working on using it for visualizing blackbox data. 

## Contributors
All work so far on **blackboxProject** has been done by Nathaniel Diamant and Nick Draper from Harvey Mudd College.
### Contributors on GitHub
* [Contributors](https://github.com/ndiamant/sw-name/graphs/contributors)
If you want to contribute by adding to the file downloading/organizing infrastrucure or analysis or if you find a bug, e-mail ndiamant@hmc.edu.

## License 
* see [LICENSE](blackboxProject/LICENSE.md) file

## How-to use this code
* see [INSTRUCTIONS](https://github.com/ndiamant/sw-name/blob/master/INSTRUCTIONS.md) file

## Contact
#### Harvey Mudd CS
* Homepage: https://www.cs.hmc.edu/research/
* e-mail: ndiamant@hmc.edu
* Twitter: [@CSTeachingTips](https://twitter.com/csteachingtips "CS Teaching Tips on twitter")
