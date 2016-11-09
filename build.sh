#!/bin/bash

# runs all unit tests and sample script
echo running unit tests ...
python -m unittest discover -s ./tests/
echo done
echo creating graphviz rendering in tm1.png ...
python rest.py | dot -Tpng -o tm1.png
echo done
