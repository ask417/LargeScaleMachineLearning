#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

##!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import ast

class PageRankAlternate(MRJob):
        
    def configure_options(self):
        super(PageRankAlternate, self).configure_options()
        self.add_passthrough_option('--iterations', type = "int", default=1)
        self.add_passthrough_option('--N', type = "int", default = -1)
        self.add_passthrough_option('--alpha', type = "float", default = .15)
    
    def __init__(self, *args, **kwargs):
        super(PageRankAlternate, self).__init__(*args, **kwargs)
        self.iterations = self.options.iterations
        self.N = self.options.N
        self.alpha = self.options.alpha
        self.loss = 0
        self.inflator = 10**10
        self.options.jobconf = {"mapred.reduce.tasks":1 }

        
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
        yield node, (links, float(1)/self.N)
        
    #Because lines are unique, each node here will occur only once 
    #If it's got links, it's not dangling, and we have 0 for dangling cell
    #if it lacks links, it is dangling, so we add it's nodeProb to dangling
    def pass_mass(self, node, line):
        links, prob = line
        #Gets called on the first iteration
        if isinstance(links, basestring):
            links = ast.literal_eval(links)
        
        numLinks = len(links)
        if numLinks == 0:
            self.loss += prob * self.inflator
            #Format: yield node, (links, passedMass, danglingLossMass)
            yield node, (links, 0)
        else:
            for link in links:
                yield link, ({}, float(prob)/numLinks)
            yield node, (links, 0)
    
    def mapper_final(self):
        yield "0", (self.loss)
    
    def combiner(self, node, lines):
        if node == "0":
            loss = sum(lines)
            yield node, loss
        else:
            nodeProb = 0
            links = {}
            for item in lines:
                link, passedMass = item 
                nodeProb+=passedMass
                if len(link)!=0:
                    links = link
            yield node, (links, nodeProb)
        
    def sum_mass(self, node, lines): 
        if node == "0":
            self.loss = sum(lines)
        else:
            loss = float(self.loss)/self.inflator
            total=0
            links = {}
            G = self.N
            a = self.alpha
            for item in lines:
                link, prob = item
                total+=prob
                if len(link) != 0:
                    links = link

            updatedProb = float(a)/G + (1-a)*(float(loss)/G + total) 
            yield node, (links, updatedProb)
            
    def steps(self):
        return (
                [MRStep(mapper=self.initialize_graph_map, 
                        combiner = self.initialize_graph_combine,
                        reducer = self.initialize_graph_reduce)] +
                [MRStep(mapper = self.pass_mass, mapper_final = self.mapper_final,
                        combiner=self.combiner,
                        reducer = self.sum_mass)] * self.options.iterations
        )
    
if __name__ == '__main__':
    PageRankAlternate.run()