#!/usr/bin/env python

#Same as above but we run on complaints data and isolate the issue column

from mrjob.job import MRJob
import re
from mrjob.step import MRStep

wordRe = re.compile(r"[\w]+")

class MRComplaintFrequencyCount(MRJob):

    MRJob.SORT_VALUES = True   

    def mapper(self, _, line):
        self.increment_counter('group','num_mapper_calls',1)
        
        #Issue is third column in csv
        issue = line.split(",")[3]
        
        for word in wordRe.findall(issue):
            yield word.lower(), 1

    def reducer(self, key, values):
        self.increment_counter('group','num_reducer_calls',1)        
        yield key, sum(values)

    def steps(self):
        JOBCONF_STEP = {
            'mapreduce.job.output.key.comparator.class': 'org.apache.hadoop.mapred.lib.KeyFieldBasedComparator',
            'stream.num.map.output.key.fields': 2,
            'mapred.text.key.comparator.options': '-k2,2nr',
        }
        return [MRStep(jobconf=JOBCONF_STEP,
                    mapper=self.mapper,
                    reducer=self.reducer)
                ]
        
if __name__ == '__main__':
    MRComplaintFrequencyCount.run()