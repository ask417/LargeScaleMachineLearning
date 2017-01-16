#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
from collections import Counter
import itertools
import re


#Goal: Take in n-gram file and output file w/ structure {Word1: {CoWord1: count1, CoWord2: count2, etc}, etc}
class BuildStripes(MRJob):
    
    def mapper(self, _, line):
        ngram, count, page, book = line.strip("\n").split("\t")
        words = ngram.split()
        
        for word in words:
            stripe = {coWord:int(count) for coWord in words if coWord != word}
            yield word, stripe
                
    def combiner(self,word, line):
        stripe = dict(reduce(lambda x,y: Counter(x)+Counter(y), line))
        yield word, stripe
    
    def reducer(self,word, line):
        stripe = dict(reduce(lambda x,y: Counter(x)+Counter(y), line))
        yield word, stripe

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer)]

if __name__=='__main__':
    BuildStripes.run()