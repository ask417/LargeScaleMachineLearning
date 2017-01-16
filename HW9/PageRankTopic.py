#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

##!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import ast
import json 

class PageRankTopic(MRJob):
        
    def configure_options(self):
        super(PageRankTopic, self).configure_options()
        self.add_passthrough_option('--iterations', type = "int", default=1)
        self.add_passthrough_option('--N', type = "int", default = -1)
        self.add_passthrough_option('--alpha', type = "float", default = .15)
        self.add_passthrough_option('--numTopics', type = "int", default = 0)
        self.add_passthrough_option('--beta', type = "float", default = .99)

    def __init__(self, *args, **kwargs):
        super(PageRankTopic, self).__init__(*args, **kwargs)
        self.iterations = self.options.iterations
        self.N = self.options.N
        self.alpha = self.options.alpha
        self.beta = self.options.beta
        self.numTopics = self.options.numTopics
        self.loss = [0]*(1+self.numTopics)
        self.options.jobconf = {"mapred.reduce.tasks":1 }
        self.nodeTopics = defaultdict(int)
        with open("topicCounts.txt", "r") as f:
            self.topicCounts = json.load(f)
        with open("randNet_topics.txt","r") as g:
            for i in g:
                node, topic = i.strip().split('\t')
                self.nodeTopics[node]=topic
        
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
        yield node, (links, [float(1)/self.N]*(1+self.numTopics))
        
    def pass_mass(self, node, line):
        links, topicProbs = line
        #Gets called on the first iteration
        if isinstance(links, basestring):
            links = ast.literal_eval(links)
        
        numLinks = len(links)
        if numLinks == 0:
            self.loss = [x + y for x, y in zip(self.loss, topicProbs)] #prob * self.inflator
            yield node, self.loss
        else:
            for link in links:
                yield link, ({}, [float(prob)/numLinks for prob in topicProbs])
            yield node, (links, [0]*(1+self.numTopics))
    
    def mapper_final(self):
        yield "0", (self.loss)
    
    def combiner(self, node, lines):
        if node == "0":
            loss = [sum(x) for x in zip(*lines)] #sum(lines)
            yield node, loss
        else:
            nodeProb = [0]*(1+self.numTopics)
            links = {}
            for item in lines:
                link, passedMass = item 
                nodeProb = [x + y for x, y in zip(nodeProb, passedMass)]
                if len(link)!=0:
                    links = link
            yield node, (links, nodeProb)
        
    def sum_mass(self, node, lines): 
        if node == "0":
            self.loss = [sum(x) for x in zip(*lines)] #sum(lines)
            #yield "lossNow", self.loss
        else:
            total=[0]*(1+self.numTopics)
            links = {}
            newProbs = []
            G = self.N
            a = self.alpha
            for item in lines:
                link, prob = item
                total= [x + y for x, y in zip(total, prob)]
                if len(link) != 0:
                    links = link

                    
            for index, value in enumerate(total):
                if str(1+index) == self.nodeTopics[node]:
                    newProbs.append(a * (float(self.beta)/self.topicCounts[self.nodeTopics[node]]) + (1-a) * (float(self.loss[index])/G + value))
                else:
                    if (index+1) == len(total):
                        newProbs.append(float(a)/G + (1-a) * (float(self.loss[index])/G + value))
                    else:
                        newProbs.append(a * (float(1-self.beta)/(G-self.topicCounts[self.nodeTopics[node]])) + (1-a) * (float(self.loss[index])/G + value))

            yield node, (links, newProbs)
            
    def steps(self):
        return (
                [MRStep(mapper = self.initialize_graph_map, 
                        combiner = self.initialize_graph_combine,
                        reducer = self.initialize_graph_reduce)] +
                [MRStep(mapper = self.pass_mass, mapper_final = self.mapper_final,
                        combiner=self.combiner,
                        reducer = self.sum_mass)] * self.options.iterations
        )
    
if __name__ == '__main__':
    PageRankTopic.run()