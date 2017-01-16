#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

from mrjob.job import MRJob
from mrjob.step import MRStep
import ast

class ShortestPathToys(MRJob):

    def configure_options(self):
        super(ShortestPathToys, self).configure_options()
        self.add_passthrough_option('--isFirstPass', type = "int", default=0)
        self.add_passthrough_option('--originNode', type = "str", default = "1")
    
    def __init__(self, *args, **kwargs):
        super(ShortestPathToys, self).__init__(*args, **kwargs)
        self.isFirstPass = self.options.isFirstPass
        self.originNode = self.options.originNode
    
    def mapper_init(self):
        try:
            # Read weights file
            with open('/Users/AnthonySpalvieriKruse/VirtualBoxShared/HW7/visited.txt', 'r') as f:
                self.visited = set(f.readlines()[0].split(','))
        except IndexError:
            self.visited = set()
        
    def mapper(self, _, line):
        node, value = line.strip().split('\t')
        node = node.strip('"') #just in case
        if self.isFirstPass:
            node, neighbors = line.strip().split("\t")
            if node == self.originNode:
                yield node, (ast.literal_eval(neighbors), 0, self.originNode, "V")
            else:
                yield node, (ast.literal_eval(neighbors), 9999999999, '', "U")
        else:
            frontier, distance, path, state = ast.literal_eval(value)
            if state == "V":
                for neighbor in frontier:
                    if neighbor not in self.visited:
                        if path:
                            yield neighbor, (None, distance+1, path+"-"+neighbor, "Q")
                        else:
                            yield neighbor, (None, distance+1, neighbor, "Q")      
            yield node, (frontier, distance, path, state)
            
    def reducer(self, key, line): 
        if self.isFirstPass:
            yield int(key), next(line)
        else:
            frontiers=[]
            distances=[]
            states=[]
            truePath=''

            for frontier, distance, path, state in line:
                frontiers.append(frontier)
                distances.append(distance)
                states.append(state)
                if path!='':
                    truePath = path

            if "Q" in states:
                if len([frontier for frontier in frontiers if frontier!=None])==0:
                    yield key, ({}, min(distances), truePath, "V")
                else:
                    yield key, ([frontier for frontier in frontiers if frontier!=None][0], min(distances), truePath, "V") 
            else:
                yield key, (frontier, distance, truePath, state)
            
    def steps(self):
        return [MRStep(mapper_init=self.mapper_init, mapper=self.mapper,reducer=self.reducer)] 
    
if __name__ == '__main__':
    ShortestPathToys.run()