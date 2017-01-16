#!/usr/bin/env python
## mapper.py
## Author: Anthony Spalvieri-Kruse
## Description: mapper that maps to tuples of all upper and lower case words 

import sys

for line in sys.stdin:
    for word in line.split():
        print '%s\t%s' % ("UpperCase" if word.istitle() else "LowerCase", 1)