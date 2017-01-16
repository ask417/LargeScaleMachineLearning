#!/usr/bin/env python

#Same as above but we run on complaints data and isolate the issue column

from mrjob.job import MRJob
import re
from mrjob.step import MRStep
from collections import defaultdict

wordRe = re.compile(r"[\w]+")

class MRComplaintFrequencyCount(MRJob):

    def mapper(self, _, line):
        self.increment_counter('group','num_mapper_calls',1)
        
        #Issue is third column in csv
        issue = line.split(",")[3]
        
        for word in wordRe.findall(issue):
            #Send all map outputs to same reducer
            yield word.lower(), 1

    def reducer(self, key, values):
        self.increment_counter('group','num_reducer_calls',1)  
        wordCounts = defaultdict(int)
        total = 0         
        for value in values:
            word, count = value
            total+=count
            wordCounts[word]+=count
            
        for k,v in wordCounts.iteritems():
            yield k, (v, float(v)/total)
        
    def combiner(self, key, values):
        self.increment_counter('group','num_combiner_calls',1) 
        yield None, (key, sum(values))
            

if __name__ == '__main__':
    MRComplaintFrequencyCount.run()