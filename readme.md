## TM1Doc
Your easy to use tm1 documenter!  
See http://www.tm1forum.com/viewtopic.php?f=3&t=12883 for discussion & stuff.

### Usage
Edit config.py to match your environment.  
You can simply run ./build.sh if you are on a linux machine.  
Otherwise use: 'python rest.py' to obtain graphviz output (can be pasted into http://www.webgraphviz.com/). Or if you have graphviz installed run 'python rest.py | dot -Tpng -o tm1.png' which should even work under windows powershell.

### Assertions
- words in Cube names start with are capital letter or can be capitalized
- you have enabled TM1s REST api (HTTPPortNumber=xxxx),
  - make sure you have configured your firewall to allow xxxx
- you have a user that is allowed to read all relevant objects on the tm1 instance
- you don't dynamically write to multiple cubes from the same process. eg. you don't do "CellputN(vCubeName, ..." where vCubename is NOT a constant.
- you assign cube names to constants in the prolog of load processes

### Dependencies
- Python, python networkx ('sudo pip install networkx'), graphviz
- tested with TM1 10.2.2 FP4
- tested with python 2.7x under windows' linux shell (http://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/)
- should run with python 3.x (maybe some print statements are wrong)
- should run natively under windows
- should run under mac os

### Feature Requests

- [ ] fix name of flatfile objects - currently backslashes from windows fs don't show
- [ ] make dimensions a valid target for processes to write to (parse for dimensionelementinsert, dimensionelementcomponentadd, attrputs, attrputn)
- [ ] create sample instance
  - steal and ammend example from big blue? Which one is good?
  - run automated integration tests on this instance
- [ ] improve test coverage (up from 0)
- [ ] use some odata library to query tm1
- [ ] create objects smarter via some json magic
- [ ] comply with Pythons PEP8 (formatting) and PEP257 (docstring)
- [ ] Rank time complexity for subgraphs
- [ ] create multiple views on the output (via python cmd interface ?)
  - Create output for D3.js (example: http://bl.ocks.org/mbostock/4339083) [Edward Stuart]
- [ ] get object sizes (including feeders ...)
  - on disk
  - in ram
- [ ] Scheduling and parallel execution of processes
  - via "packages" as independent components of the dataflow graph
  - via knapsack-like optimizer
    - general case is NP hard
    - in this case greedy should work brilliantly
  - add estimated runtime
  - maybe create input file for cubewises hustle (https://hustle.codeplex.com/) needs c#/.net :(  
- [ ] logfile parser
  - integrate into class objects?
- [ ] Add Source Code Control system via git & REST
  - also use it as a form of CI
  - maybe simple cmd line script to push process from filesystem to server via rest api?
- [ ] perform various model checks
  - unused
    - dimensions
    - cubes
    - processes
    - groups
  - high feeder:data ratio
  - automated "overfeeding"-cubes (http://www.ibm.com/developerworks/data/library/cognos/financial_management/analytics/page620.html #5)
  - cube and dimension filesizes
  - dimension: one element consolidations
  - dimension: hierarchy checks
  - dimension: elements without data and rule calculations (feeder flags)
    - unused element ratio = elements with data / all elements
  - cube: dimension order and sparsity checks
  - load time analysis
    - cubes
    - feeders (rules)
  - empty subsets


- [x] create possibility for processes to have multiple targets
- [x] get ignore_tech_objecs to work
- [x] make the output graph pretty (dimensions clutter it up)
- [x] Check whether MultiDIGraph makes sense -> nope!
- [x] Dimension and Dimension -> Cube mapping
- [x] REST Connection


### Usefull Links
- description of REST API: http://swagger-ui.cubeac.com/#/
- alternative, easy tool written in PERL by some smart person: http://www.bihints.com/graphing_tm1_data_flow
- usefull regex playground: https://regex101.com/
