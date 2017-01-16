#!/usr/bin/env python

import sys
from collections import defaultdict

spamWords=0
hamWords=0
lines = []
    
for line in sys.stdin:
    lines.append(line)
    word, spam, ham = line.split()
    spamWords+=float(spam)
    hamWords+=float(ham)
    
for line in lines:
    word, spam, ham = line.split()
    spamProb = str(0 if spamWords==0 else float(spam)/int(spamWords))
    hamProb = str(0 if hamWords==0 else float(ham)/int(hamWords))
    print '%s\t%s\t%s' % (word, spamProb, hamProb)