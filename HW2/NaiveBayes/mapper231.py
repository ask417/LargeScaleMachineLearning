#!/usr/bin/env python

import sys
import re
from collections import defaultdict

spam = defaultdict(int)
ham = defaultdict(int)
words = set()


for line in sys.stdin:
    spamOrHam = "spam" if line.split()[1]=="1" else "ham"
    for word in re.findall(r'[a-z/\']+', line.lower())[1:]:  #line.split() previously 
        words.add(word)
        if spamOrHam == "spam":
            spam[word]+=1
        elif spamOrHam == "ham":
            ham[word]+=1

for word in words:
    print '%s\t%s\t%s' % (word, ham[word],spam[word])    