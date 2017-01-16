#!/usr/bin/env python
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol
import re    
 
class top5pages(MRJob):
    
    OUTPUT_PROTOCOL = RawValueProtocol
    
    pages = ["NA","NA","NA","NA","NA"]
    counts = [0,0,0,0,0]

    def steps(self):
        return [MRStep(
                mapper = self.mapper,
                combiner = self.combiner,
                reducer = self.reducer,
                reducer_final = self.reducer_final
                )]
    
    def mapper(self, _, line):
        data = re.split(",",line)
        pageID = data[1]
        yield pageID,1
        
    def combiner(self,pageID,counts):
        count = sum(counts)
        yield pageID,count

    def reducer(self,pageID,counts):
        count = sum(counts)
        ix = -1
        for i in range(5):
            if count > self.counts[i]:
                ix = i
            else:
                break

        if ix >= 0:
            self.counts.insert(ix+1,count)
            self.pages.insert(ix+1,pageID)
            self.counts = self.counts[1:6]
            self.pages = self.pages[1:6]

    def reducer_final(self):
        self.counts.reverse()
        self.pages.reverse()
        print "The top 5 pages are:"
        for i in range(5):
            yield None,self.pages[i] + "," + str(self.counts[i])

if __name__ == '__main__':
    top5pages.run()