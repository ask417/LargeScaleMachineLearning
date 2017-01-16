#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

##!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import ast

class PageRankScale(MRJob):
        
    def configure_options(self):
        super(PageRankScale, self).configure_options()
        self.add_passthrough_option('--N', type = "int", default = -1)
        self.add_passthrough_option('--alpha', type = "float", default = .15)
        self.add_passthrough_option('--loss', type = "float", default = 0)
    
    def __init__(self, *args, **kwargs):
        super(PageRankScale, self).__init__(*args, **kwargs)
        self.N = self.options.N
        self.alpha = self.options.alpha
        self.inflator = 10**12
        self.loss = float(self.options.loss)/self.inflator

    def pass_mass(self, node, line):
        node, linksAndProb = map(lambda x: ast.literal_eval(x), line.split('\t'))
        links, prob = linksAndProb
        if isinstance(links, basestring):
            links = ast.literal_eval(links)
            
        numLinks = len(links)
        for link in links:
            yield link, ({}, float(prob)/numLinks)
        yield node, (links, 0)
    
    
    def combiner(self, node, lines):
        nodeProb = 0
        links = {}
        for item in lines:
            link, passedMass = item 
            nodeProb+=passedMass
            if len(link)!=0:
                links = link
        yield node, (links, nodeProb)
        
    def sum_mass(self, node, lines): 
        total=0
        links = {}
        G = self.N
        a = self.alpha
        for item in lines:
            link, prob = item
            total+=prob
            if len(link) != 0:
                links = link

        updatedProb = float(a)/G + (1-a)*(float(self.loss)/G + total) 
        
        if len(links) == 0:
            self.increment_counter('loss', 'lossCounter', int(self.inflator*updatedProb))

        yield node, (links, updatedProb)
            
    def steps(self):
        return (
            [MRStep(mapper = self.pass_mass,
                        combiner=self.combiner,
                        reducer = self.sum_mass)]
        )
    
if __name__ == '__main__':
    PageRankScale.run()