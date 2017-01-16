#!/usr/bin/env python

import sys
import math
from collections import defaultdict

spamWords=0
hamWords=0
totalWords=0
lines = []
    
for line in sys.stdin:
    lines.append(line)
    key, label, wordCount, notImp1, notImp2 = line.split()
    totalWords+=float(wordCount)
    if int(label)==1:
        spamWords+=float(wordCount)
    else:
        hamWords+=float(wordCount)

spamProb = math.log(sys.float_info.epsilon + float(spamWords)/totalWords)
hamProb = math.log(sys.float_info.epsilon + float(hamWords)/totalWords)
        
for line in lines:
    key, label, wordCount, hamProbCond, spamProbCond = line.split()
    probs = (float(hamProbCond)+hamProb, float(spamProbCond)+spamProb)
    
    if probs[0]==probs[1]:
        predLabel = 1 if spamProb > hamProb else 0
    else:
        predLabel = 1 if probs[0] > probs[1] else 0 
    
    print "%s\t%s" % (key, predLabel)
    
    