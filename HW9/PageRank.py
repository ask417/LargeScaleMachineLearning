#!/usr/bin/env python
##!/Users/AnthonySpalvieriKruse/anaconda/bin/python

from mrjob.job import MRJob
from mrjob.step import MRStep
import ast

class PageRank(MRJob):

    def configure_options(self):
        super(PageRank, self).configure_options()
        self.add_passthrough_option('--iterations', type = "int", default=1)
        self.add_passthrough_option('--N', type = "int", default = -1)
        self.add_passthrough_option('--alpha', type = "float", default = .15)
    
    def __init__(self, *args, **kwargs):
        super(PageRank, self).__init__(*args, **kwargs)
        self.iterations = self.options.iterations
        self.N = self.options.N
        self.alpha = self.options.alpha
    
    def initialize_graph(self, _, line):
        node, links = line.strip().split("\t")
        yield node, (links, float(1)/self.N)
        
    def pass_mass(self, node, line):
        links, prob = line
        
        #Gets called on the first iteration
        if isinstance(links, basestring):
            links = ast.literal_eval(links)
        
        numLinks = len(links)
        if numLinks == 0:
            yield "dangling", prob
        else:
            for link in links:
                yield link, prob/numLinks

        yield node, links
    
    def combiner(self, node, lines):
        if node == "dangling":
            yield node, sum(lines)
        else:
            total = 0 
            links = {}
            for item in lines:
                if type(item) is float:
                    total+=item
                else:
                    links = item
                    yield node, links
            yield node, total
        
    def sum_mass(self, node, lines): 
        if node == "dangling":
            loss = sum(lines)
            #This assumes the nodes are indexed, which could fail
            #Better idea is to pass file w/ all nodes, and iterate through this list
            for i in range(1, int(self.options.N) + 1):
                yield str(i), loss
        else:
            total = 0 
            links = {}
            for item in lines:
                if type(item) is float:
                    total+=item
                else:
                    links = item
            yield node, (links, total)
    
    def teleport(self, node, lines):
        G = self.N
        a = self.alpha
        loss = 0
        
        for item in lines:
            if type(item) == float:
                loss = item
            else:
                links, prob = item
            
        updatedProb = float(a)/G + (1-a)*(float(loss)/G + prob) 
        yield node, (links, updatedProb)
    
    def steps(self):
        return (
                [MRStep(mapper=self.initialize_graph)] +
                [MRStep(mapper = self.pass_mass, combiner=self.combiner, reducer = self.sum_mass),
                 MRStep(reducer = self.teleport)] * self.options.iterations
        )
    
if __name__ == '__main__':
    PageRank.run()