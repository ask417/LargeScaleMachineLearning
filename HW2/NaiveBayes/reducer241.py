#!/usr/bin/env python

import sys
from collections import defaultdict

spamD = defaultdict(int)
hamD = defaultdict(int)
spamWords=0
hamWords=0
words = set()
    
for line in sys.stdin:
    word, ham, spam = line.split()
    spamD[word]+=float(spam)
    hamD[word]+=float(ham)
    spamWords+=float(spam)
    hamWords+=float(ham)
    words.add(word)

vocabSize = len(words)

for word in words:
    spamProb = str(0 if spamWords==0 else (float(spamD[word])+1)/(int(spamWords) + vocabSize))
    hamProb = str(0 if hamWords==0 else (float(hamD[word])+1)/(int(hamWords) + vocabSize))
    print '%s\t%s\t%s' % (word, hamProb, spamProb)