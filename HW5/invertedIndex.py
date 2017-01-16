#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
from collections import Counter
import json
import itertools
import re


#Goal: Take in key {strip} file, and output inversion of {word: {doc1: wordsInDoc1, doc2: etc}, etc}
class InvertedIndex(MRJob):
    
    def mapper(self, _, line):
        doc, stripe = line.strip("\n").split("\t")
        stripe = json.loads(stripe)
        stripeLength = len(stripe)
        
        for word in stripe.keys():
            yield word, {doc.strip('"'): stripeLength}
                
    def combiner(self,word, line):
        #A bit overkill because keys won't appear twice, but still combines it
        stripe = dict(reduce(lambda x,y: Counter(x)+Counter(y), line))
        yield word, stripe
    
    def reducer(self,word, line):
        stripe = dict(reduce(lambda x,y: Counter(x)+Counter(y), line))
        yield word, stripe

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer)]

if __name__=='__main__':
    InvertedIndex.run()