#!/usr/bin/env python

#Mapper and reducer with mrjob just counting calls to each component, just using single line text

from mrjob.job import MRJob
from mrjob.step import MRStep
import re

wordRe = re.compile(r"[\w]+")

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        self.increment_counter('group','num_mapper_calls',1)
        for word in wordRe.findall(line):
            yield word.lower(), 1

    def reducer(self, key, values):
        self.increment_counter('group','num_reducer_calls',1)        
        yield key, sum(values)


if __name__ == '__main__':
    MRWordFrequencyCount.run()