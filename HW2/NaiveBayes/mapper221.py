#!/usr/bin/env python
## mapper.py
## Author: Anthony Spalvieri-Kruse
## Description: mapper that maps to tuples of all upper and lower case words 

import sys
import re

for line in sys.stdin:
    spamOrHam = "spam" if line.split()[1]=="1" else "ham"
    for word in re.findall(r'[a-z/\']+', line.lower()):  #line.split() previously 
        print '%s\t%s' % (word+"_"+spamOrHam, 1)