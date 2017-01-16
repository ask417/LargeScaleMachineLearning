#!/usr/bin/env python

import sys
import re
import math
from collections import defaultdict

def jointProbability(hamSpamTuples):
    
    spamSum = 0
    hamSum = 0 
    
    for hamSpamTuple in hamSpamTuples:
        ham = hamSpamTuple[0]
        spam = hamSpamTuple[1]
        spamSum += math.log(spam + sys.float_info.epsilon)
        hamSum += math.log(ham + sys.float_info.epsilon)
    
    return (hamSum, spamSum)

modelProbs = defaultdict(tuple)
spam = defaultdict(int)
ham = defaultdict(int)
words = set()

#Don't forget to rerun the model so that ham and spam aren't mixed up 
with open("chineseModel.tsv") as f:
    model = f.readlines()
    for line in model:
        word, ham, spam = line.split()
        modelProbs[word] = (float(ham), float(spam))

for line in sys.stdin:
    cp = line.split()
    key = cp[0]
    label = cp[1]
    email = cp[2:]
    email = " ".join(cp[2:])
    email = re.findall(r'[a-z/\']+',email.lower())
    numWords = len(email)
    email = [modelProbs[word] for word in email]
    email = [word if word!=() else (0,0) for word in email]
    #probs = reduce(lambda x,y : (x[0]*y[0],x[1]*y[1]),email)
    probs = jointProbability(email)
    print "%s\t%s\t%s\t%s\t%s" % (key, label, numWords, probs[0], probs[1])