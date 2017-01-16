#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

from mrjob.job import MRJob
from mrjob.step import MRStep
import ast
import itertools

class EDA(MRJob):
    
    def configure_options(self):
        super(EDA, self).configure_options()
        self.add_passthrough_option('--feature', type = "str")
        
    def __init__(self, *args, **kwargs):
        super(EDA, self).__init__(*args, **kwargs)
        self.feature = self.options.feature
        self.nodes = set()
        self.frequency = 0 
        self.numLinks = 0
        self.minDegree = 0
        self.maxDegree = 0 
        self.options.jobconf = {"mapred.reduce.tasks":1 }
        
    def mapper(self, key, line):
        node, neighbors = line.strip().split("\t")
        neighbors = ast.literal_eval(neighbors)
        numLinks = len(neighbors)
        self.nodes.add(node)
        for neighbor in neighbors:
            self.nodes.add(neighbor)

        if self.feature == "Nodes" or self.feature == "numNodes":
            for neighbor in neighbors:
                yield neighbor, 1
            yield node, 1
        elif self.feature == "numLinks":
            yield node, numLinks
        elif self.feature == "averageDegree":
            yield node, numLinks
        elif self.feature == "minMaxDegree":
            yield None, numLinks
        else:
            print "Acceptable features: numNodes, numLinks, averageDegree, minMaxDegree"
            exit()
            
    def combiner(self, key, values):
        if self.feature == "Nodes" or self.feature == "numNodes":
            yield key, 1
        elif self.feature == "numLinks":
            yield key, sum(values)
        elif self.feature == "averageDegree":
            yield key, sum(values)
        elif self.feature == "minMaxDegree":
            values, valuesCp = itertools.tee(values)
            yield None, (min(values), max(valuesCp))
        
    def reducer(self, key, values):
        if self.feature == "Nodes" or self.feature == "numNodes":
            self.frequency+=1
            self.nodes.add(key)
        elif self.feature == "numLinks":
            self.numLinks += sum(values)
        elif self.feature == "averageDegree":  
            self.frequency+=1
            self.numLinks += sum(values)
        elif self.feature == "minMaxDegree":
            values, valuesCp = itertools.tee(values)
            self.maxDegree = max(values)
            self.minDegree = min(valuesCp)
    
    def reducer_final(self):
        if self.feature == "numNodes":
            yield "Number of Nodes: ", self.frequency
        elif self.feature == "numLinks":
            yield "Number of Links", self.numLinks
        elif self.feature == "averageDegree":
            yield "Average Degree: ", float(self.numLinks)/self.frequency
        elif self.feature == "minMaxDegree":
            yield "Min/Max Degree: ", (self.minDegree, self.maxDegree)
        elif self.feature == "Nodes":
            yield "", [node for node in self.nodes]
        
    
    def steps(self):
        return [MRStep(mapper=self.mapper,reducer=self.reducer,
                      reducer_final=self.reducer_final)] 
    
if __name__ == '__main__':
    EDA.run()