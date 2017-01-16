#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

from mrjob.job import MRJob
from mrjob.step import MRStep
import ast

class Identity(MRJob):
    
    def mapper(self, _, value):
        key, value = value.strip().split('\t')
        yield key, ast.literal_eval(value)
    def steps(self):
        return [MRStep(mapper=self.mapper)] 
    
if __name__ == '__main__':
    Identity.run()