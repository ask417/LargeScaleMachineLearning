#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import itertools
import re

class NgramEDA(MRJob):
    
    
    
    def configure_options(self):
        super(NgramEDA, self).configure_options()
        self.add_passthrough_option("--feature_type", type="str")
        self.add_passthrough_option("--topN", type="int")
    
    def __init__(self, *args, **kwargs):
        super(NgramEDA, self).__init__(*args, **kwargs)
        self.feature_type = self.options.feature_type
        self.topN = self.options.topN
        self.ngram = ["nada" for i in range(self.topN)]
        self.frequencies = [0 for i in range(self.topN)]
        
    def mapper(self, key, line):
        title, count, pages, books = line.strip("\n").split("\t")
        words = title.split()
        numChar = len(title)
        
        if self.feature_type == "length":
            yield None, numChar
        if self.feature_type == "frequency":
            for word in words:
                yield word, int(count)
        if self.feature_type == "density":
            for word in words:
                yield word, (int(count),int(pages))
        if self.feature_type == "distribution":
            yield str(numChar), 1    
                    
    def reducer(self, key, counts):
        if self.feature_type == "length":
            yield "Max Length", max(counts)
        if self.feature_type == "frequency":
            total = sum(counts)
            ix = -1
            for i in range(len(self.frequencies)):
                if total > self.frequencies[i]:
                    ix = i
                else:
                    break
            if ix >= 0:
                self.frequencies.insert(ix+1,total)
                self.ngram.insert(ix+1,key)
                self.frequencies = self.frequencies[1:(1+len(self.frequencies))]
                self.ngram = self.ngram[1:(1+len(self.frequencies))]
            #yield key, total
        if self.feature_type == "density":
            count, pages = map(sum,zip(*counts))
            yield key, float(count)/pages
        if self.feature_type == "distribution":
            yield key, sum(counts)
        
    def reducer_final(self):
        if self.feature_type == "frequency":
            self.frequencies.reverse()
            self.ngram.reverse()
            print "The top 10000 pages are:"
            for i in range(self.topN):
                yield self.ngram[i] , self.frequencies[i]

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer, reducer_final=self.reducer_final)]

if __name__=='__main__':
    NgramEDA.run()