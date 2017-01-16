#!/usr/bin/env python

import sys
from collections import defaultdict

spamD = defaultdict(int)
hamD = defaultdict(int)
spamWords=0
hamWords=0
allWords = set()
filteredWords = set()

for line in sys.stdin:
    word, ham, spam = line.split()
    spamD[word]+=float(spam)
    hamD[word]+=float(ham)
    allWords.add(word)
    
#Smoothing parameter should count the vocabSize after filtering
for word in allWords:
    if hamD[word]+spamD[word] >= 3:
        filteredWords.add(word)
        spamWords+=spamD[word]
        hamWords+=hamD[word]

vocabSize = len(filteredWords)

for word in filteredWords:
    if hamD[word]+spamD[word] >= 3:
        spamProb = str(0 if spamWords==0 else (float(spamD[word])+1)/(int(spamWords) + vocabSize))
        hamProb = str(0 if hamWords==0 else (float(hamD[word])+1)/(int(hamWords) + vocabSize))
        print '%s\t%s\t%s' % (word, hamProb, spamProb)