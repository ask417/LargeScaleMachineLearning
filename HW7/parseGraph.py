#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

from mrjob.job import MRJob
from mrjob.step import MRStep
import ast

class ParseGraph(MRJob):

    def configure_options(self):
        super(ParseGraph, self).configure_options()
        self.add_passthrough_option('--originNode', type = "str")
    
    def __init__(self, *args, **kwargs):
        super(ParseGraph, self).__init__(*args, **kwargs)
        self.originNode = self.options.originNode
        
    def mapper(self, key, line):
        node, neighbors = line.strip().split("\t")
        if node == self.originNode:
            yield node, (ast.literal_eval(neighbors), 0, self.originNode, "V")
        else:
            yield node, (ast.literal_eval(neighbors), 9999999999, '', "U")
            
    def reducer(self, key, line): 
        #neighbors, distance, path, state = next(line)
        #yield key, (neighbors, distance, path, state)
        yield key, next(line)
            
    def steps(self):
        return [MRStep(mapper=self.mapper,
                       reducer=self.reducer)] 
    
if __name__ == '__main__':
    ParseGraph.run()