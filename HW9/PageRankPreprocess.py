#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

##!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import ast

class PageRankPreprocess(MRJob):
        
    def configure_options(self):
        super(PageRankPreprocess, self).configure_options()
        self.add_passthrough_option('--N', type = "int", default = -1)
    
    def __init__(self, *args, **kwargs):
        super(PageRankPreprocess, self).__init__(*args, **kwargs)
        self.N = self.options.N
        self.inflator = 10**12
        
    def initialize_graph_map(self, _, line):
        node, links = line.strip().split("\t")
        links = ast.literal_eval(links)
        for link in links:
            yield link, {}
        yield node, links
        
    def initialize_graph_combine(self, node, lines):
        links = {}
        for item in lines:
            if len(item)!=0:
                links = item
        yield node, links
    
    def initialize_graph_reduce(self, node, lines):
        links = {}
        for item in lines:
            if len(item)!=0:
                links = item
        #if dangling increment loss counter
        if len(links) == 0:
            self.increment_counter('loss', 'lossCounter', int(self.inflator*float(1)/self.N))

        yield node, (links, float(1)/self.N)
            
    def steps(self):
        return (
                [MRStep(mapper=self.initialize_graph_map, 
                        combiner = self.initialize_graph_combine,
                        reducer = self.initialize_graph_reduce)] 
        )
    
if __name__ == '__main__':
    PageRankPreprocess.run()