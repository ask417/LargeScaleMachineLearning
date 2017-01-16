#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
from collections import Counter
import json
import itertools
import re
import math


#Goal: Take in key {strip} file, and output inversion of {word: {doc1: wordsInDoc1, doc2: etc}, etc}
class PairwiseSimilarity(MRJob):
    
    #For future reference, if this is too large to store in memory
    #we can hack it.  Tack the union sum onto the end of the sorted key
    #and then parse it all out at the reducer stage
    unions = defaultdict(int)
    
    def configure_options(self):
        super(PairwiseSimilarity, self).configure_options()
        self.add_passthrough_option("--similarity_measure", type="str")
    
    def __init__(self, *args, **kwargs):
        super(PairwiseSimilarity, self).__init__(*args, **kwargs)
        self.similarity_measure = self.options.similarity_measure
        
    def mapper(self, _, line):
        doc, stripe = line.strip("\n").split("\t")
        stripe = json.loads(stripe)
        stripeLength = len(stripe)
        
        if self.similarity_measure == "jaccard":
            pairs = map(dict, itertools.combinations(stripe.items(),2))
            for pair in pairs:
                key = sorted(pair.keys()) # ",".join(sorted(pair.keys()))
                self.unions[",".join(key)]=sum(pair.values())
                yield key, 1
        if self.similarity_measure == "cosine":
            pairs = map(dict, itertools.combinations(stripe.items(),2))
            for pair in pairs:
                key = sorted(pair.keys()) # ",".join(sorted(pair.keys()))
                normProduct = reduce(lambda x,y: math.sqrt(x)*math.sqrt(y), pair.values())
                yield key, float(1)/normProduct
                
    def combiner(self,key, values):
        
        if self.similarity_measure == "jaccard":
            yield key, sum(values) 
        if self.similarity_measure == "cosine":
            yield key, sum(values)
    
    def reducer(self,key, values):
        totalCount = sum(values)
        if self.similarity_measure == "jaccard":
            similarity = float(totalCount)/(self.unions[",".join(key)] - totalCount) #float(counts + singleCount)/union
            yield key, similarity
        if self.similarity_measure == "cosine":
            yield key, totalCount
            
    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer)]

if __name__=='__main__':
    PairwiseSimilarity.run()