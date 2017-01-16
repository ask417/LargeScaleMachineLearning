#!/usr/bin/env python

import sys
import re
from collections import defaultdict

spam = defaultdict(int)
ham = defaultdict(int)
words = set()


#Modify this so that you don't count the key; key is not the same as subject line
for line in sys.stdin:
    cp = line.split()
    label = cp[1]
    email = cp[2:]
    email = " ".join(cp[2:])
    spamOrHam = "spam" if label=="1" else "ham"
    for word in re.findall(r'[a-z/\']+', email.lower()):  #line.split() previously 
        words.add(word)
        if spamOrHam == "spam":
            spam[word]+=1
        elif spamOrHam == "ham":
            ham[word]+=1

for word in words:
    print '%s\t%s\t%s' % (word, ham[word],spam[word])